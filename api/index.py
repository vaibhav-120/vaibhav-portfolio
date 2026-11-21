"""FastAPI backend for the portfolio's voice agent.

POST /api/ask      {"question": str, "history": [...], "voice": bool, "stream": bool}
  stream=true  (default) -> Server-Sent Events: model, sentence (+ audio), done, error
  stream=false           -> JSON {"answer": str, "model": str}  (used by the evals)
GET  /api/health   -> {"ok": true, "voice": bool, "models": [...]}
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request  # noqa: E402
from fastapi.responses import JSONResponse, StreamingResponse  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from _lib import agent, ratelimit, tts  # noqa: E402

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
tts.warm()


class Turn(BaseModel):
    role: str
    content: str


class Ask(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    history: list[Turn] = Field(default_factory=list, max_length=12)
    voice: bool = True
    stream: bool = True


def _client_key(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    return fwd.split(",")[0].strip() or request.headers.get("x-real-ip", "") or "anon"


def _sse(event: str, data: dict) -> bytes:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n".encode()


@app.get("/api/health")
async def health():
    return {"ok": True, "voice": tts.available(), "models": agent.MODELS}


@app.post("/api/ask")
async def ask(body: Ask, request: Request):
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

    speak = body.voice and tts.available()

    async def events():
        loop = asyncio.get_running_loop()
        try:
            yield _sse("ready", {"serverVoice": speak})
            async for ev in agent.answer_sentences(question, history):
                if ev["type"] == "model":
                    yield _sse("model", {"model": ev["model"]})
                    continue
                payload = {"text": ev["text"]}
                if speak:
                    try:
                        wav = await loop.run_in_executor(None, tts.synthesize_wav, ev["text"])
                        payload["audio"] = base64.b64encode(wav).decode()
                    except Exception:
                        pass  # The browser falls back to its own voice for this sentence.
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
