#!/usr/bin/env python3
"""
Setup verification script for Chatterbox TTS Local Deployment
"""
import subprocess
import sys
import importlib
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.9+")
        return False

def check_uv_installation():
    """Check if UV is installed"""
    print("📦 Checking UV installation...")
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ UV installed: {result.stdout.strip()}")
            return True
        else:
            print("   ❌ UV not found")
            return False
    except FileNotFoundError:
        print("   ❌ UV not installed")
        print("   💡 Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False

def check_virtual_environment():
    """Check if virtual environment exists"""
    print("🏠 Checking virtual environment...")
    venv_path = Path("chatterbox-env")
    if venv_path.exists():
        print("   ✅ Virtual environment 'chatterbox-env' found")
        return True
    else:
        print("   ❌ Virtual environment not found")
        print("   💡 Create with: uv venv chatterbox-env")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📚 Checking dependencies...")
    required_packages = [
        'torch',
        'torchaudio', 
        'transformers',
        'fastapi',
        'streamlit',
        'librosa',
        'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print("   💡 Install missing packages with: uv pip install --python chatterbox-env/bin/python -r requirements.txt")
        return False
    return True

def check_chatterbox_package():
    """Check if Chatterbox package is installed"""
    print("🗣️ Checking Chatterbox TTS...")
    try:
        from chatterbox.tts import ChatterboxTTS
        print("   ✅ Chatterbox TTS package imported successfully")
        return True
    except ImportError as e:
        print(f"   ❌ Cannot import Chatterbox TTS: {e}")
        print("   💡 Install with: uv pip install --python chatterbox-env/bin/python -e . --no-deps")
        return False

def check_file_structure():
    """Check if required files exist"""
    print("📁 Checking file structure...")
    required_files = [
        'fastapi_tts_server.py',
        'streamlit_app.py',
        'requirements.txt',
        'run_fastapi.sh',
        'run_streamlit.sh',
        'test_tts.py'
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_device_compatibility():
    """Check device compatibility"""
    print("🖥️ Checking device compatibility...")
    try:
        import torch
        if torch.backends.mps.is_available():
            print("   ✅ MPS (Apple Silicon) acceleration available")
        elif torch.cuda.is_available():
            print("   ✅ CUDA acceleration available")
        else:
            print("   ⚠️ CPU-only mode (slower but functional)")
        return True
    except ImportError:
        print("   ❌ Cannot check device compatibility - PyTorch not installed")
        return False

def main():
    """Run all verification checks"""
    print("🔍 Chatterbox TTS Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("UV Package Manager", check_uv_installation),
        ("Virtual Environment", check_virtual_environment),
        ("Dependencies", check_dependencies),
        ("Chatterbox Package", check_chatterbox_package),
        ("File Structure", check_file_structure),
        ("Device Compatibility", check_device_compatibility),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print()
        if check_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your setup is ready to go!")
        print()
        print("🚀 Next steps:")
        print("   1. Start FastAPI server: ./run_fastapi.sh &")
        print("   2. Start Streamlit app: ./run_streamlit.sh")
        print("   3. Open http://localhost:8501 in your browser")
    else:
        print("❌ Some checks failed. Please address the issues above.")
        print()
        print("📖 For detailed setup instructions, see README.md")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
