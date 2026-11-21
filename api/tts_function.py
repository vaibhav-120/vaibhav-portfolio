"""Speech function for the portfolio's voice agent: turns one sentence into audio.

Kept separate from api/index.py so loading the voice model can never slow down
the conversation itself.

GET  /api/tts           -> loads the voice if needed (warm-up) and reports status
POST /api/tts {"text"}  -> audio/wav for that text
"""

from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request  # noqa: E402
from fastapi.responses import JSONResponse, Response  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from _lib import ratelimit, tts  # noqa: E402

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Separate, more generous bucket than questions: every answer is several sentences.
_limiter = ratelimit.Limiter(max_requests=int(os.environ.get("TTS_RATE_LIMIT_MAX", "150")))


class Speak(BaseModel):
    text: str = Field(min_length=1, max_length=400)


def _client_key(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    return fwd.split(",")[0].strip() or request.headers.get("x-real-ip", "") or "anon"


# Plain `def` endpoints run in FastAPI's thread pool, so loading or synthesizing
# never blocks other requests on the same instance.
@app.get("/api/tts")
def status():
    if tts.disabled():
        return {"voice": False, "reason": "disabled"}
    try:
        tts.get_voice()
        return {"voice": True, "loadMs": tts.load_ms()}
    except Exception as e:
        return JSONResponse({"voice": False, "reason": f"{type(e).__name__}: {e}"}, status_code=503)


@app.post("/api/tts")
def speak(body: Speak, request: Request):
    if tts.disabled():
        return JSONResponse({"error": "voice disabled"}, status_code=503)
    if not _limiter.allow(_client_key(request)):
        return JSONResponse({"error": "rate limited"}, status_code=429)
    try:
        t = time.perf_counter()
        wav = tts.synthesize_wav(body.text)
        synth_ms = round((time.perf_counter() - t) * 1000)
    except Exception as e:
        print(f"[tts] synthesis failed: {type(e).__name__}: {e}", file=sys.stderr, flush=True)
        return JSONResponse({"error": "voice unavailable"}, status_code=503)
    return Response(
        wav,
        media_type="audio/wav",
        headers={"Cache-Control": "no-store", "X-Synth-Ms": str(synth_ms)},
    )