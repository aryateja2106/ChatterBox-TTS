#!/bin/bash
echo "================================================"
echo "🚀 Starting FastAPI Server (Backend)"
echo "================================================"
echo "📍 Server URL: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🔄 Health Check: http://localhost:8000/health"
echo ""
echo "📝 NOTE: This will download AI models on first run (~3GB)"
echo "⏳ This may take 5-10 minutes initially..."
echo ""
source chatterbox-env/bin/activate && python fastapi_tts_server.py
