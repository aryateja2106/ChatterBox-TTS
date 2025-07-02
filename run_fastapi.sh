#!/bin/bash
echo "Starting Chatterbox TTS FastAPI server using uv..."
uv run --python chatterbox-env/bin/python fastapi_tts_server.py
