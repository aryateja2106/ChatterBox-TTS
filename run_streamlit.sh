#!/bin/bash
echo "Starting Chatterbox TTS Streamlit app using uv..."
uv run --python chatterbox-env/bin/python -m streamlit run streamlit_app.py
