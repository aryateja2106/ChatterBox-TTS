#!/bin/bash
echo "🚀 Starting Chatterbox TTS FastAPI server with UV..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📚 API docs will be at: http://localhost:8000/docs"
echo ""
uv run --python chatterbox-env/bin/python fastapi_tts_server.py
