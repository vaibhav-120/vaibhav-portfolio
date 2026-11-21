"""Piper text-to-speech. Runs on CPU inside the Vercel function.

The voice model (~60 MB) is too big to ship inside the Vercel function, so:
  - locally, it's read from api/_data/voices/ (run scripts/download-voice.sh), and
  - on Vercel, it's downloaded to /tmp in the background when an instance starts.

Until the voice is ready (or if it can't be loaded), `ready()` is False and the
browser speaks the reply with its built-in voice instead, so the agent still works.
"""

from __future__ import annotations

import io
import os
import re
import sys
import threading
import time
import wave
from pathlib import Path

import httpx

VOICE_NAME = os.environ.get("PIPER_VOICE", "en_US-lessac-medium")
BUNDLED_DIR = Path(__file__).resolve().parent.parent / "_data" / "voices"
CACHE_DIR = Path(os.environ.get("PIPER_CACHE_DIR", "/tmp/piper-voices"))
VOICE_BASE_URL = os.environ.get(
    "PIPER_VOICE_BASE_URL",
    "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium",
)

_voice = None
_state = "idle"  # idle -> loading -> ready | failed
_failed_at = 0.0
RETRY_AFTER = 120  # seconds before retrying a failed load
_lock = threading.Lock()


def _log(msg: str) -> None:
    print(f"[tts] {msg}", file=sys.stderr, flush=True)


def _local_model() -> Path | None:
    p = BUNDLED_DIR / f"{VOICE_NAME}.onnx"
    if p.exists() and (BUNDLED_DIR / f"{VOICE_NAME}.onnx.json").exists():
        return p
    return None


def _download_model() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    model = CACHE_DIR / f"{VOICE_NAME}.onnx"
    for name in (f"{VOICE_NAME}.onnx.json", f"{VOICE_NAME}.onnx"):
        dest = CACHE_DIR / name
        if dest.exists():
            continue
        tmp = dest.with_suffix(dest.suffix + ".part")
        with httpx.stream("GET", f"{VOICE_BASE_URL}/{name}", follow_redirects=True, timeout=60) as r:
            r.raise_for_status()
            with open(tmp, "wb") as f:
                for chunk in r.iter_bytes(1 << 20):
                    f.write(chunk)
        tmp.rename(dest)
    return model


def _load() -> None:
    global _voice, _state, _failed_at
    try:
        path = _local_model() or _download_model()
        from piper import PiperVoice

        _voice = PiperVoice.load(path)
        _state = "ready"
        _log(f"voice ready: {path}")
    except Exception as e:  # network error, bad file, missing package
        _state = "failed"
        _failed_at = time.monotonic()
        _log(f"voice unavailable, browser voice will be used: {type(e).__name__}: {e}")


def warm() -> None:
    """Start loading the voice in the background. Never blocks a request."""
    global _state
    if os.environ.get("PIPER_DISABLED") == "1":
        _state = "failed"
        return
    with _lock:
        retry = _state == "failed" and time.monotonic() - _failed_at > RETRY_AFTER
        if _state != "idle" and not retry:
            return
        _state = "loading"
    threading.Thread(target=_load, daemon=True).start()


def ready() -> bool:
    return _state == "ready"


def status() -> str:
    return _state


def _speakable(text: str) -> str:
    text = text.replace("~", "about ")
    text = re.sub(r"(\d)\s*ms\b", r"\1 milliseconds", text)
    text = re.sub(r"(\d)\s*s\b", r"\1 seconds", text)
    return text


def synthesize_wav(text: str) -> bytes:
    if _voice is None:
        raise RuntimeError("voice not ready")
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        first = True
        for chunk in _voice.synthesize(_speakable(text)):
            if first:
                wav.setnchannels(chunk.sample_channels)
                wav.setsampwidth(chunk.sample_width)
                wav.setframerate(chunk.sample_rate)
                first = False
            wav.writeframes(chunk.audio_int16_bytes)
        if first:  # no audio produced
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(22050)
    return buf.getvalue()