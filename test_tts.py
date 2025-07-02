#!/usr/bin/env python3
"""
Quick test to verify Chatterbox TTS works on Mac
"""
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

def test_tts():
    print("Testing Chatterbox TTS on Mac...")
    
    # Detect device (Mac with M1/M2/M3/M4)
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    
    try:
        # Initialize model
        print("Loading model...")
        model = ChatterboxTTS.from_pretrained(device=device)
        print("Model loaded successfully!")
        
        # Test text
        text = "Hello, this is a test of Chatterbox TTS on Mac!"
        print(f"Generating speech for: {text}")
        
        # Generate audio
        wav = model.generate(text)
        print(f"Generated audio with shape: {wav.shape}")
        print(f"Sample rate: {model.sr}")
        
        # Save test audio
        output_file = "test_output.wav"
        ta.save(output_file, wav, model.sr)
        print(f"Audio saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_tts()
    if success:
        print("✅ TTS test completed successfully!")
    else:
        print("❌ TTS test failed!")
