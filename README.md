# 🗣️ ChatterBox TTS Web App

**Turn text into speech with voice cloning - through a simple web interface**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> Built by **Arya Teja Rudraraju** | Powered by [Resemble AI's Chatterbox](https://github.com/resemble-ai/chatterbox)

## What is this?

This is a **web application** that lets you:
1. **Type text** → Get speech audio
2. **Upload your voice** → Clone any voice 
3. **Use an API** → Integrate with your apps

Instead of complicated command-line tools, you get a simple website that just works.

## Why did I build this?

Resemble AI created amazing text-to-speech technology, but it was hard to use. I wanted:
- ✅ A simple website instead of terminal commands
- ✅ Easy voice cloning with drag & drop
- ✅ Fast performance on Mac computers
- ✅ API endpoints for developers

## 🚀 How to Run

### Step 1: Install Requirements
```bash
# Install UV package manager (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Make sure you have Python 3.9+
python --version
```

### Step 2: Get the Code
```bash
git clone https://github.com/aryateja2106/ChatterBox-TTS.git
cd ChatterBox-TTS
```

### Step 3: Install Everything
```bash
# Create environment and install dependencies (this takes a few minutes)
uv venv chatterbox-env
source chatterbox-env/bin/activate
uv pip install --python chatterbox-env/bin/python -r requirements.txt
uv pip install --python chatterbox-env/bin/python -e . --no-deps
```

### Step 4: Start the App
```bash
# Make scripts executable
chmod +x run_fastapi.sh run_streamlit.sh

# Open Terminal 1 and run:
./run_fastapi.sh

# Open Terminal 2 and run:
./run_streamlit.sh
```

### Step 5: Use the App
- **Open your browser**: http://localhost:8501
- **Type some text** and click "Generate Speech"
- **Done!** Your audio will appear below

### Extra: API Access
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎭 How to Use

### Basic Text-to-Speech
1. Open the web interface at http://localhost:8501
2. Type your text in the input box
3. Adjust parameters if needed (exaggeration, pace, etc.)
4. Click "Generate Speech"
5. Listen to the result and download if desired

### Voice Cloning
1. Check the "Upload reference audio for voice cloning" box
2. Upload a clear audio sample (3-30 seconds)
3. Enter your text
4. Generate speech with the cloned voice

### API Integration
```python
import requests
import base64

# Generate speech via API
response = requests.post(
    "http://localhost:8000/synthesize",
    json={"text": "Hello, world!", "exaggeration": 0.5}
)

if response.status_code == 200:
    data = response.json()
    audio_bytes = base64.b64decode(data["audio_base64"])
    with open("output.wav", "wb") as f:
        f.write(audio_bytes)
```

## ⚙️ Configuration

### Key Parameters
- **Exaggeration** (0.25-2.0): Controls emotional intensity
- **CFG/Pace** (0.0-1.0): Controls generation guidance and pacing
- **Temperature** (0.05-5.0): Controls randomness in generation

### Voice Cloning Tips
- Use clear, noise-free audio samples
- 5-15 seconds duration works best
- WAV format recommended
- Single speaker only

## 🔧 Troubleshooting

### Common Issues
- **Port conflicts**: Check if ports 8000/8501 are free
- **Memory issues**: Close other apps, use shorter text
- **MPS not available**: Update to macOS 12.3+ for Apple Silicon

### Performance
- **Apple Silicon Macs**: 5-15 seconds generation time
- **Intel/Other systems**: 15-45 seconds generation time

## 🛠️ Development

### Using UV for Development
```bash
# Run tests
uv run --python chatterbox-env/bin/python test_tts.py

# Start servers with UV
uv run --python chatterbox-env/bin/python fastapi_tts_server.py
uv run --python chatterbox-env/bin/python -m streamlit run streamlit_app.py
```

### Project Structure
```
ChatterBox-TTS/
├── fastapi_tts_server.py    # FastAPI backend
├── streamlit_app.py         # Streamlit frontend  
├── requirements.txt         # Dependencies
├── test_tts.py             # Basic tests
├── run_fastapi.sh          # Server startup script
├── run_streamlit.sh        # UI startup script
└── src/chatterbox/         # Core TTS package
```

## 🙏 Credits

This project is built on top of the incredible work by **Resemble AI**:
- Original Chatterbox TTS: https://github.com/resemble-ai/chatterbox
- Amazing technology that makes this all possible
- Special thanks to their team for making this open source

**Additional acknowledgments:**
- Hugging Face for model hosting
- FastAPI and Streamlit communities
- All the contributors to the original Chatterbox project

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

This project uses Resemble AI's Chatterbox TTS model, which is also licensed under MIT.

## ⚠️ Responsible Use

- Only clone voices with proper consent
- This tool is for legitimate and ethical use cases
- Generated audio includes watermarking for responsible AI

---

**Made with ❤️ by Arya Teja Rudraraju**  
*Bringing state-of-the-art TTS to everyone through modern web interfaces*
