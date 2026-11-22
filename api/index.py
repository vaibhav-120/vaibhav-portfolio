"""Conversation function for the portfolio's voice agent. Text only: it never
loads the voice, so nothing heavy can slow it down. Speech is made by api/tts.py.

POST /api/ask      {"question": str, "history": [...], "stream": bool}
  stream=true  (default) -> Server-Sent Events: ready, model, sentence, done, error
  stream=false           -> JSON {"answer": str, "model": str}  (used by the evals)
GET  /api/health   -> {"ok": true, "models": [...]}   (?warm=1 also opens the Groq connection)
"""

from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request  # noqa: E402
from fastapi.responses import JSONResponse, StreamingResponse  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from _lib import agent, ratelimit  # noqa: E402
from _lib.tts_routes import router as tts_router  # noqa: E402

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(tts_router)
_requests_served = 0  # 0 on a freshly started (cold) instance


class Turn(BaseModel):
    role: str
    content: str


class Ask(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    history: list[Turn] = Field(default_factory=list, max_length=12)
    stream: bool = True
    voice: bool = True  # accepted for compatibility; speech is handled by /api/tts


def _client_key(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    return fwd.split(",")[0].strip() or request.headers.get("x-real-ip", "") or "anon"


def _sse(event: str, data: dict) -> bytes:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n".encode()


@app.get("/api/health")
async def health(warm: int = 0):
    if warm:
        await agent.warm_connection()
    return {"ok": True, "models": agent.MODELS}


@app.post("/api/ask")
async def ask(body: Ask, request: Request):
    global _requests_served
    if not ratelimit.allow(_client_key(request)):
        return JSONResponse(
            {"error": "Too many questions for now. Please try again in a few minutes."},
            status_code=429,
        )

    history = [t.model_dump() for t in body.history]
    question = body.question.strip()

    if not body.stream:
        parts: list[str] = []
        model = ""
        try:
            async for ev in agent.answer_sentences(question, history):
                if ev["type"] == "model":
                    model = ev["model"]
                else:
                    parts.append(ev["text"])
        except agent.NoModelAvailable:
            return JSONResponse({"answer": agent.FALLBACK_REPLY, "model": ""}, status_code=503)
        return {"answer": " ".join(parts), "model": model}

    cold = _requests_served == 0
    _requests_served += 1
    t_start = time.perf_counter()

    def ms() -> int:
        return round((time.perf_counter() - t_start) * 1000)

    async def events():
        first = True
        first_token_ms = 0
        try:
            yield _sse("ready", {"cold": cold})
            async for ev in agent.answer_sentences(question, history):
                if ev["type"] == "model":
                    first_token_ms = ms()
                    yield _sse("model", {"model": ev["model"]})
                    continue
                payload = {"text": ev["text"]}
                if first:
                    first = False
                    payload["timing"] = {
                        "firstToken": first_token_ms,
                        "firstSentence": ms(),
                        "cold": cold,
                    }
                yield _sse("sentence", payload)
            yield _sse("done", {})
        except agent.NoModelAvailable:
            yield _sse("error", {"message": agent.FALLBACK_REPLY})
        except Exception:
            yield _sse("error", {"message": "Something went wrong. Please try again."})

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )