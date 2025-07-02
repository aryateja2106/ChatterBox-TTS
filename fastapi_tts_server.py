#!/usr/bin/env python3
"""
FastAPI server for Chatterbox TTS with Mac support
"""
import os
import io
import base64
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import torch
import torchaudio as ta
import numpy as np
from chatterbox.tts import ChatterboxTTS
import tempfile
from typing import Optional

# Global model instance
model = None

class TTSRequest(BaseModel):
    text: str
    exaggeration: float = 0.5
    cfg_weight: float = 0.5
    temperature: float = 0.8
    repetition_penalty: float = 1.2
    min_p: float = 0.05
    top_p: float = 1.0

class TTSResponse(BaseModel):
    message: str
    audio_base64: Optional[str] = None
    sample_rate: int

def init_model():
    """Initialize the TTS model with Mac support"""
    global model
    if model is None:
        print("Initializing Chatterbox TTS model...")
        
        # Detect best device for Mac
        if torch.backends.mps.is_available():
            device = "mps"
            print("Using MPS (Apple Silicon GPU)")
        else:
            device = "cpu"
            print("Using CPU")
        
        # Initialize model
        model = ChatterboxTTS.from_pretrained(device=device)
        print(f"Model loaded successfully on {device}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_model()
    yield
    # Shutdown
    pass

# Create FastAPI app with lifespan
app = FastAPI(
    title="Chatterbox TTS API", 
    version="1.0.0",
    description="A modern API for text-to-speech with voice cloning capabilities",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Chatterbox TTS API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    global model
    return {
        "status": "healthy" if model is not None else "model_not_loaded",
        "device": "mps" if torch.backends.mps.is_available() else "cpu",
        "torch_version": torch.__version__
    }

@app.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(request: TTSRequest):
    """
    Synthesize speech from text using the default voice
    """
    global model
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 500:
        raise HTTPException(status_code=400, detail="Text too long (max 500 characters)")
    
    try:
        print(f"Generating speech for: {request.text[:50]}...")
        
        # Generate audio
        wav = model.generate(
            text=request.text,
            exaggeration=request.exaggeration,
            cfg_weight=request.cfg_weight,
            temperature=request.temperature,
            repetition_penalty=request.repetition_penalty,
            min_p=request.min_p,
            top_p=request.top_p,
        )
        
        # Convert to base64 for JSON response
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            ta.save(temp_file.name, wav, model.sr)
            
            with open(temp_file.name, "rb") as audio_file:
                audio_base64 = base64.b64encode(audio_file.read()).decode()
            
            os.unlink(temp_file.name)
        
        return TTSResponse(
            message="Speech synthesized successfully",
            audio_base64=audio_base64,
            sample_rate=model.sr
        )
        
    except Exception as e:
        print(f"Error during synthesis: {e}")
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")

@app.post("/synthesize_with_voice")
async def synthesize_with_voice(
    text: str,
    voice_file: UploadFile = File(...),
    exaggeration: float = 0.5,
    cfg_weight: float = 0.5,
    temperature: float = 0.8,
    repetition_penalty: float = 1.2,
    min_p: float = 0.05,
    top_p: float = 1.0
):
    """
    Synthesize speech with a custom voice prompt
    """
    global model
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not initialized")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Validate file type
    if not voice_file.filename.lower().endswith(('.wav', '.mp3', '.flac', '.m4a')):
        raise HTTPException(status_code=400, detail="Voice file must be audio format (wav, mp3, flac, m4a)")
    
    try:
        # Save uploaded voice file temporarily
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_voice:
            content = await voice_file.read()
            temp_voice.write(content)
            temp_voice_path = temp_voice.name
        
        print(f"Generating speech with custom voice for: {text[:50]}...")
        
        # Generate audio with voice prompt
        wav = model.generate(
            text=text,
            audio_prompt_path=temp_voice_path,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            min_p=min_p,
            top_p=top_p,
        )
        
        # Clean up voice file
        os.unlink(temp_voice_path)
        
        # Convert to bytes for streaming response
        with tempfile.NamedTemporaryFile(suffix=".wav") as temp_output:
            ta.save(temp_output.name, wav, model.sr)
            temp_output.seek(0)
            audio_bytes = temp_output.read()
        
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=synthesized_speech.wav"}
        )
        
    except Exception as e:
        print(f"Error during synthesis with voice: {e}")
        # Clean up on error
        if 'temp_voice_path' in locals():
            try:
                os.unlink(temp_voice_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")

@app.get("/download_audio/{base64_audio}")
async def download_audio(base64_audio: str):
    """
    Download audio from base64 string
    """
    try:
        audio_bytes = base64.b64decode(base64_audio)
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=synthesized_speech.wav"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid audio data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("Starting Chatterbox TTS FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
