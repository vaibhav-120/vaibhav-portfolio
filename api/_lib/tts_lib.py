"""Piper text-to-speech, used only by the api/tts.py function.

The voice model (~60 MB) is too big to ship inside a Vercel function, so:
  - locally, it's read from api/_data/voices/ (run scripts/download-voice.sh), and
  - on Vercel, the first request on a new instance downloads it to /tmp.

Loading happens inside a request (the widget sends a warm-up request when the
visitor presses Start), never in a background thread, because Vercel only gives
a function CPU while it's handling a request.
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
_lock = threading.Lock()
_load_ms = 0


def _log(msg: str) -> None:
    print(f"[tts] {msg}", file=sys.stderr, flush=True)


def disabled() -> bool:
    return os.environ.get("PIPER_DISABLED") == "1"


def _model_path() -> Path:
    local = BUNDLED_DIR / f"{VOICE_NAME}.onnx"
    if local.exists() and (BUNDLED_DIR / f"{VOICE_NAME}.onnx.json").exists():
        return local
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
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
    return CACHE_DIR / f"{VOICE_NAME}.onnx"


def get_voice():
    """Load the voice once per instance. Blocks the calling request until ready."""
    global _voice, _load_ms
    if _voice is not None:
        return _voice
    with _lock:
        if _voice is None:
            t = time.perf_counter()
            from piper import PiperVoice

            _voice = PiperVoice.load(_model_path())
            _load_ms = round((time.perf_counter() - t) * 1000)
            _log(f"voice {VOICE_NAME} loaded in {_load_ms} ms")
    return _voice


def ready() -> bool:
    return _voice is not None


def load_ms() -> int:
    return _load_ms


def _speakable(text: str) -> str:
    text = text.replace("~", "about ")
    text = re.sub(r"(\d)\s*ms\b", r"\1 milliseconds", text)
    text = re.sub(r"(\d)\s*s\b", r"\1 seconds", text)
    return text


def synthesize_wav(text: str) -> bytes:
    voice = get_voice()
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        first = True
        for chunk in voice.synthesize(_speakable(text)):
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