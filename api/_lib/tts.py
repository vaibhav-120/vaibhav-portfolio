"""Piper text-to-speech. Runs on CPU inside the Vercel function.

If no voice model is present, `available()` is False and the browser speaks the
reply with its built-in voice instead, so the agent still works.
"""

from __future__ import annotations

import io
import os
import re
import threading
import wave
from pathlib import Path

VOICE_DIR = Path(__file__).resolve().parent.parent / "_data" / "voices"
VOICE_NAME = os.environ.get("PIPER_VOICE", "en_US-lessac-medium")

_voice = None
_lock = threading.Lock()
_failed = False


def _model_path() -> Path:
    return VOICE_DIR / f"{VOICE_NAME}.onnx"


def available() -> bool:
    return not _failed and _model_path().exists()


def _load():
    global _voice, _failed
    if _voice is not None:
        return _voice
    with _lock:
        if _voice is None:
            try:
                from piper import PiperVoice

                _voice = PiperVoice.load(_model_path())
            except Exception:
                _failed = True
                raise
    return _voice


def warm() -> None:
    """Load the voice early so the first visitor doesn't pay the load time."""
    if available():
        try:
            _load()
        except Exception:
            pass


def _speakable(text: str) -> str:
    text = text.replace("~", "about ")
    text = re.sub(r"(\d)\s*ms\b", r"\1 milliseconds", text)
    text = re.sub(r"(\d)\s*s\b", r"\1 seconds", text)
    return text


def synthesize_wav(text: str) -> bytes:
    voice = _load()
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
