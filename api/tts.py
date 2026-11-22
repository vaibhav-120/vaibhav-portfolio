"""Dedicated Vercel function for Piper speech synthesis."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI  # noqa: E402

from _lib.tts_routes import router  # noqa: E402

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(router)