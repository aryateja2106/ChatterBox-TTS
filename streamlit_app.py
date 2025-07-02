import streamlit as st
import requests
import base64
import time
import os
from io import BytesIO

# Set the FastAPI endpoints
FASTAPI_SYNTHESIZE_ENDPOINT = "http://localhost:8000/synthesize"
FASTAPI_VOICE_CLONE_ENDPOINT = "http://localhost:8000/synthesize_with_voice"
FASTAPI_HEALTH_ENDPOINT = "http://localhost:8000/health"

# Page configuration
st.set_page_config(
    page_title="Chatterbox TTS",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(90deg, #FF6B35 0%, #F7931E 100%);
    color: white;
    margin-bottom: 2rem;
    border-radius: 10px;
}
.parameter-section {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}
.generate-button {
    background-color: #FF6B35;
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 0.5rem 2rem;
    border: none;
    cursor: pointer;
}
.stAudio {
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🗣️ Chatterbox TTS</h1>
    <p>State-of-the-art Text-to-Speech with Voice Cloning</p>
</div>
""", unsafe_allow_html=True)

# Check server status
with st.sidebar:
    st.header("🔧 Server Status")
    try:
        health_response = requests.get(FASTAPI_HEALTH_ENDPOINT, timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ Server is running")
            st.info(f"Device: {health_data.get('device', 'Unknown')}")
            st.info(f"PyTorch: {health_data.get('torch_version', 'Unknown')}")
        else:
            st.error("❌ Server not responding")
    except:
        st.error("❌ Cannot connect to server")
        st.warning("Please start the FastAPI server first:\n```bash\n./run_fastapi.sh\n```")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Text Input")
    text_input = st.text_area(
        "Text to synthesize (max chars 500)",
        value="Now let's make my mum's favourite. So three mars bars into the pan. Then we add the tuna and just stir for a bit, just let the chocolate and fish infuse. A sprinkle of olive oil and some tomato ketchup. Now smell that. Oh boy this is going to be incredible.",
        height=150,
        max_chars=500,
        help="Enter the text you want to convert to speech"
    )
    
    char_count = len(text_input)
    color = "red" if char_count > 500 else "green" if char_count > 400 else "blue"
    st.markdown(f"<p style='color: {color}; font-size: 0.8em;'>Characters: {char_count}/500</p>", unsafe_allow_html=True)

with col2:
    st.header("🎵 Output Audio")
    audio_placeholder = st.empty()
    
    with audio_placeholder.container():
        st.info("Generated audio will appear here")

# Voice cloning section
st.header("🎭 Voice Cloning (Optional)")
use_voice_cloning = st.checkbox("Upload reference audio for voice cloning", help="Upload an audio file to clone a specific voice")

reference_audio = None
if use_voice_cloning:
    col_ref1, col_ref2 = st.columns([2, 1])
    
    with col_ref1:
        reference_audio = st.file_uploader(
            "Reference Audio File",
            type=['wav', 'mp3', 'flac', 'm4a'],
            help="Upload a clear audio sample (3-30 seconds recommended)"
        )
    
    with col_ref2:
        if reference_audio:
            st.audio(reference_audio, format='audio/wav')
            st.success(f"📁 {reference_audio.name}")
            file_size = len(reference_audio.getvalue()) / (1024 * 1024)
            st.info(f"Size: {file_size:.1f} MB")

# Parameters section
st.header("⚙️ Generation Parameters")

col_param1, col_param2 = st.columns(2)

with col_param1:
    st.subheader("Primary Controls")
    exaggeration = st.slider(
        "Exaggeration (Neutral = 0.5, extreme values can be unstable)",
        min_value=0.25,
        max_value=2.0,
        value=0.5,
        step=0.05,
        help="Controls emotional intensity and expression"
    )
    
    cfg_weight = st.slider(
        "CFG/Pace",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Controls generation guidance and pacing"
    )

with col_param2:
    st.subheader("Advanced Controls")
    with st.expander("More options", expanded=False):
        seed_num = st.number_input(
            "Random seed (0 for random)",
            min_value=0,
            max_value=999999,
            value=0,
            help="Set a specific seed for reproducible results"
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.05,
            max_value=5.0,
            value=0.8,
            step=0.05,
            help="Controls randomness in generation"
        )
        
        min_p = st.slider(
            "Min P (Newer Sampler, 0.02-0.1 recommended)",
            min_value=0.0,
            max_value=1.0,
            value=0.05,
            step=0.01,
            help="Minimum probability threshold for token selection"
        )
        
        top_p = st.slider(
            "Top P (1.0 disables, original sampler)",
            min_value=0.0,
            max_value=1.0,
            value=1.0,
            step=0.01,
            help="Nucleus sampling parameter"
        )
        
        repetition_penalty = st.slider(
            "Repetition Penalty",
            min_value=1.0,
            max_value=2.0,
            value=1.2,
            step=0.1,
            help="Penalty for repeating tokens"
        )

# Generate button
st.markdown("<br>", unsafe_allow_html=True)
generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])

with generate_col2:
    if st.button("🚀 Generate Speech", use_container_width=True, type="primary"):
        if not text_input.strip():
            st.error("❌ Please enter some text to synthesize.")
        elif len(text_input) > 500:
            st.error("❌ Text is too long. Please limit to 500 characters.")
        else:
            with st.spinner("🎙️ Generating speech... This may take a moment."):
                try:
                    start_time = time.time()
                    
                    if use_voice_cloning and reference_audio:
                        # Use voice cloning endpoint
                        files = {
                            'voice_file': (reference_audio.name, reference_audio.getvalue(), reference_audio.type)
                        }
                        data = {
                            'text': text_input,
                            'exaggeration': exaggeration,
                            'cfg_weight': cfg_weight,
                            'temperature': temperature,
                            'repetition_penalty': repetition_penalty,
                            'min_p': min_p,
                            'top_p': top_p
                        }
                        
                        response = requests.post(
                            FASTAPI_VOICE_CLONE_ENDPOINT,
                            files=files,
                            data=data,
                            timeout=300  # 5 minutes timeout
                        )
                        
                        if response.status_code == 200:
                            audio_bytes = response.content
                            generation_time = time.time() - start_time
                            
                            with audio_placeholder.container():
                                st.success(f"✅ Speech generated successfully in {generation_time:.1f}s")
                                st.audio(audio_bytes, format="audio/wav")
                                
                                # Download button
                                st.download_button(
                                    label="📥 Download Audio",
                                    data=audio_bytes,
                                    file_name=f"chatterbox_voice_clone_{int(time.time())}.wav",
                                    mime="audio/wav"
                                )
                        else:
                            error_msg = response.json().get('detail', 'Unknown error') if response.headers.get('content-type') == 'application/json' else 'Server error'
                            st.error(f"❌ Error: {error_msg}")
                    
                    else:
                        # Use default voice endpoint
                        response = requests.post(
                            FASTAPI_SYNTHESIZE_ENDPOINT,
                            json={
                                "text": text_input,
                                "exaggeration": exaggeration,
                                "cfg_weight": cfg_weight,
                                "temperature": temperature,
                                "repetition_penalty": repetition_penalty,
                                "min_p": min_p,
                                "top_p": top_p
                            },
                            timeout=300  # 5 minutes timeout
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            audio_bytes = base64.b64decode(data["audio_base64"])
                            generation_time = time.time() - start_time
                            
                            with audio_placeholder.container():
                                st.success(f"✅ Speech generated successfully in {generation_time:.1f}s")
                                st.audio(audio_bytes, format="audio/wav")
                                
                                # Download button
                                st.download_button(
                                    label="📥 Download Audio",
                                    data=audio_bytes,
                                    file_name=f"chatterbox_tts_{int(time.time())}.wav",
                                    mime="audio/wav"
                                )
                        else:
                            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
                            st.error(f"❌ Error: {error_data.get('detail', 'Unknown error')}")
                            
                except requests.exceptions.Timeout:
                    st.error("⏰ Request timed out. The text might be too long or the server is busy.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to the server. Please make sure the FastAPI server is running.")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🤖 Powered by <strong>Chatterbox TTS</strong> by Resemble AI</p>
    <p>Built with FastAPI + Streamlit • Voice cloning capabilities included</p>
</div>
""", unsafe_allow_html=True)
