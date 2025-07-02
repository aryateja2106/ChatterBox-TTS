#!/bin/bash
echo "================================================"
echo "🎨 Starting Streamlit Web App (Frontend)"
echo "================================================"
echo "📍 Web App: http://localhost:8501"
echo ""
echo "⚠️ IMPORTANT: Make sure FastAPI server is running first!"
echo "   (Run ./run_fastapi.sh in another terminal)"
echo ""
echo "📦 Starting web interface..."
echo ""
source chatterbox-env/bin/activate && streamlit run streamlit_app.py
