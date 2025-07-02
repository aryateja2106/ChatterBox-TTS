#!/bin/bash
echo "🎨 Starting Chatterbox TTS Streamlit interface with UV..."
echo "📍 Web interface will be available at: http://localhost:8501"
echo "🎙️ Make sure FastAPI server is running first!"
echo ""
uv run --python chatterbox-env/bin/python -m streamlit run streamlit_app.py
