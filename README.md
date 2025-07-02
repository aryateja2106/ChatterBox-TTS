
<img width="1200" alt="cb-big2" src="https://github.com/user-attachments/assets/bd8c5f03-e91d-4ee5-b680-57355da204d1" />

# 🗣️ Chatterbox TTS - Local Deployment

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Discord](https://img.shields.io/discord/1377773249798344776?label=join%20discord&logo=discord&style=flat)](https://discord.gg/rJq9cRJBJ6)

A production-ready local deployment of **Chatterbox TTS** by Resemble AI with FastAPI backend and Streamlit frontend, featuring voice cloning capabilities and optimized for Apple Silicon Macs.

_Made with ♥️ by [Resemble AI](https://resemble.ai) | Enhanced for local deployment_

## ✨ Features

- 🎯 **State-of-the-art TTS**: Based on Resemble AI's Chatterbox model
- 🎭 **Voice Cloning**: Upload reference audio to clone any voice
- 🚀 **Apple Silicon Optimized**: Automatic MPS acceleration on M1/M2/M3/M4 Macs
- 🔄 **FastAPI Backend**: RESTful API for easy integration
- 🎨 **Beautiful UI**: Streamlit-based web interface
- ⚙️ **Advanced Controls**: Emotion exaggeration, temperature, CFG weight, and more
- 📦 **Easy Setup**: One-command installation with UV package manager
- 🔒 **Secure**: Isolated virtual environment with pinned dependencies

## 🖼️ Screenshots

### Main Interface
The Streamlit interface provides an intuitive way to generate speech with various parameters:

- **Text Input**: Support for up to 500 characters
- **Voice Cloning**: Optional reference audio upload
- **Parameter Controls**: Exaggeration, CFG/Pace, temperature, and advanced sampling options
- **Real-time Preview**: Instant audio playback and download

### API Documentation
FastAPI automatically generates interactive API documentation available at `http://localhost:8000/docs`

## 🛠️ Prerequisites

- **Python**: 3.9 or higher
- **macOS**: Recommended (optimized for Apple Silicon)
- **UV Package Manager**: For fast, reliable dependency management
- **Git**: For cloning the repository

### Install UV (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd chatterbox-tts
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment with UV
uv venv chatterbox-env

# Activate the environment
source chatterbox-env/bin/activate
```

### 3. Install Dependencies

```bash
# Install all dependencies using UV (much faster than pip)
uv pip install --python chatterbox-env/bin/python -r requirements.txt

# Install the Chatterbox package in development mode
uv pip install --python chatterbox-env/bin/python -e . --no-deps
```

### 4. Start the Services

#### Option A: Using the provided scripts (Recommended)

```bash
# Make scripts executable
chmod +x run_fastapi.sh run_streamlit.sh

# Start FastAPI server (in background)
./run_fastapi.sh &

# Start Streamlit app (in foreground)
./run_streamlit.sh
```

#### Option B: Manual startup

```bash
# Terminal 1: Start FastAPI server
source chatterbox-env/bin/activate
python fastapi_tts_server.py

# Terminal 2: Start Streamlit app
source chatterbox-env/bin/activate
streamlit run streamlit_app.py
```

### 5. Access the Application

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## 📋 Detailed Setup Guide

### System Requirements

- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space for models
- **Network**: Internet connection for initial model download

### First Run

On the first run, the system will:
1. Download the Chatterbox TTS models (~3.2GB total)
2. Initialize the voice encoder and speech tokenizer
3. Load the models into memory

**Note**: Initial model download may take 5-10 minutes depending on your internet connection.

### Performance Optimization

#### Apple Silicon Macs (M1/M2/M3/M4)
- Automatically uses MPS (Metal Performance Shaders) for GPU acceleration
- Typical generation time: 5-15 seconds for moderate text length

#### Intel Macs / Other Systems
- Falls back to CPU processing
- Typical generation time: 15-45 seconds for moderate text length

## 🎛️ API Usage

### Basic Text-to-Speech

```bash
curl -X POST "http://localhost:8000/synthesize" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello, this is a test of Chatterbox TTS!",
       "exaggeration": 0.5,
       "cfg_weight": 0.5,
       "temperature": 0.8
     }'
```

### Voice Cloning

```bash
curl -X POST "http://localhost:8000/synthesize_with_voice" \
     -F "text=Hello, this is my cloned voice!" \
     -F "voice_file=@reference_audio.wav" \
     -F "exaggeration=0.7" \
     -F "cfg_weight=0.3"
```

### Python Integration

```python
import requests
import base64

# Basic TTS
response = requests.post(
    "http://localhost:8000/synthesize",
    json={
        "text": "Your text here",
        "exaggeration": 0.5,
        "cfg_weight": 0.5
    }
)

if response.status_code == 200:
    data = response.json()
    audio_bytes = base64.b64decode(data["audio_base64"])
    
    # Save audio file
    with open("output.wav", "wb") as f:
        f.write(audio_bytes)
```

## ⚙️ Configuration Parameters

### Core Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `exaggeration` | 0.25-2.0 | 0.5 | Controls emotional intensity and expression |
| `cfg_weight` | 0.0-1.0 | 0.5 | Classifier-free guidance weight (affects pacing) |
| `temperature` | 0.05-5.0 | 0.8 | Sampling temperature (creativity vs consistency) |

### Advanced Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `repetition_penalty` | 1.0-2.0 | 1.2 | Penalty for token repetition |
| `min_p` | 0.0-1.0 | 0.05 | Minimum probability threshold |
| `top_p` | 0.0-1.0 | 1.0 | Nucleus sampling parameter |

### Parameter Tuning Tips

- **For natural speech**: `exaggeration=0.5`, `cfg_weight=0.5`
- **For expressive speech**: `exaggeration=0.7-1.0`, `cfg_weight=0.3-0.4`
- **For fast speakers**: Lower `cfg_weight` to 0.3
- **For dramatic content**: Higher `exaggeration` (0.8+)

## 🎭 Voice Cloning Guide

### Preparing Reference Audio

**Best Practices:**
- **Duration**: 3-30 seconds (optimal: 5-15 seconds)
- **Quality**: Clear, noise-free recording
- **Content**: Single speaker, natural speech
- **Format**: WAV preferred, MP3/FLAC/M4A supported

**Supported Formats:**
- WAV (recommended)
- MP3
- FLAC
- M4A

### Voice Cloning Workflow

1. **Record/Upload Reference**: Use a clear sample of the target voice
2. **Set Parameters**: Adjust `exaggeration` and `cfg_weight` for best results
3. **Generate**: Process your text with the cloned voice
4. **Fine-tune**: Adjust parameters if needed for better quality

## 🔧 Troubleshooting

### Common Issues

#### Server Won't Start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Kill existing process if needed
kill -9 <PID>
```

#### Model Download Fails
```bash
# Clear cache and retry
rm -rf ~/.cache/huggingface/
python test_tts.py
```

#### Memory Issues
- **Reduce batch size**: Use shorter text inputs
- **Close other applications**: Free up RAM
- **Check available memory**: 
  ```bash
  # macOS
  vm_stat
  ```

#### MPS Not Available
If you see "MPS not available" on Apple Silicon:
- Update to macOS 12.3+
- Update PyTorch: `pip install torch torchaudio --upgrade`

### Performance Issues

#### Slow Generation
1. **Check device**: Verify MPS is being used (check logs)
2. **Reduce text length**: Break long texts into smaller chunks
3. **Adjust parameters**: Lower `temperature` and `exaggeration`

#### Poor Quality Output
1. **Check reference audio**: Ensure it's clear and noise-free
2. **Adjust parameters**: Try different `cfg_weight` values
3. **Experiment with settings**: Test various parameter combinations

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export CHATTERBOX_DEBUG=1
python fastapi_tts_server.py
```

## 📁 Project Structure

```
chatterbox-tts/
├── src/chatterbox/           # Core TTS package
├── fastapi_tts_server.py     # FastAPI backend server
├── streamlit_app.py          # Streamlit frontend
├── requirements.txt          # Python dependencies
├── test_tts.py              # Basic functionality test
├── run_fastapi.sh           # FastAPI startup script
├── run_streamlit.sh         # Streamlit startup script
├── chatterbox-env/          # Virtual environment
└── README.md               # This file
```

## 🔒 Security Considerations

- **Local Only**: Servers bind to localhost by default
- **File Upload**: Reference audio files are processed locally and cleaned up
- **No Data Persistence**: Generated audio is not stored permanently
- **Isolated Environment**: Uses virtual environment for dependency isolation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Resemble AI** for the original Chatterbox TTS model
- **Hugging Face** for model hosting and transformers library
- **FastAPI** and **Streamlit** communities for excellent frameworks
- **Original Chatterbox Contributors**:
  - [Cosyvoice](https://github.com/FunAudioLLM/CosyVoice)
  - [Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
  - [HiFT-GAN](https://github.com/yl4579/HiFTNet)
  - [Llama 3](https://github.com/meta-llama/llama3)
  - [S3Tokenizer](https://github.com/xingchensong/S3Tokenizer)

## 🔐 Built-in PerTh Watermarking for Responsible AI

Every audio file generated by Chatterbox includes [Resemble AI's Perth (Perceptual Threshold) Watermarker](https://github.com/resemble-ai/perth) - imperceptible neural watermarks that survive MP3 compression, audio editing, and common manipulations while maintaining nearly 100% detection accuracy.

### Watermark extraction

```python
import perth
import librosa

AUDIO_PATH = "YOUR_FILE.wav"

# Load the watermarked audio
watermarked_audio, sr = librosa.load(AUDIO_PATH, sr=None)

# Initialize watermarker (same as used for embedding)
watermarker = perth.PerthImplicitWatermarker()

# Extract watermark
watermark = watermarker.get_watermark(watermarked_audio, sample_rate=sr)
print(f"Extracted watermark: {watermark}")
# Output: 0.0 (no watermark) or 1.0 (watermarked)
```

## 📞 Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions and community support
- **Original Discord**: 👋 Join [Resemble AI's Discord](https://discord.gg/rJq9cRJBJ6) for model-specific questions

## 🚀 What's Next?

- [ ] Docker containerization
- [ ] Multiple voice presets
- [ ] Batch processing capabilities
- [ ] Real-time streaming
- [ ] Integration examples for popular frameworks

## ⚠️ Disclaimer

This tool is intended for legitimate and ethical use cases only. Please ensure you have proper consent before cloning someone's voice. The original training data comes from freely available sources on the internet.

---

**Made with ❤️ for the open source community**
