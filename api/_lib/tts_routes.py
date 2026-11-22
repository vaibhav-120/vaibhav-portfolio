"""Routes shared by the local API and the dedicated Vercel TTS function."""

from __future__ import annotations

import os
import sys
import time

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field

from . import ratelimit, tts_lib as tts

router = APIRouter()

# Separate, more generous bucket than questions: every answer is several sentences.
_limiter = ratelimit.Limiter(max_requests=int(os.environ.get("TTS_RATE_LIMIT_MAX", "150")))


class Speak(BaseModel):
    text: str = Field(min_length=1, max_length=400)


def _client_key(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    return fwd.split(",")[0].strip() or request.headers.get("x-real-ip", "") or "anon"


@router.get("/api/tts")
def status():
    if tts.disabled():
        return {"voice": False, "reason": "disabled"}
    try:
        tts.get_voice()
        return {"voice": True, "loadMs": tts.load_ms()}
    except Exception as e:
        return JSONResponse({"voice": False, "reason": f"{type(e).__name__}: {e}"}, status_code=503)


@router.post("/api/tts")
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