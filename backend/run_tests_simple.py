"""
Simple test runner for Windows that sets up the environment properly.
"""
import os
import sys
import subprocess

def setup_environment():
    """Set up the testing environment."""
    # Get the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(backend_dir, 'src')
    
    # Add to Python path
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    # Set environment variables for testing
    test_env = os.environ.copy()
    test_env.update({
        'DATABASE_URL': 'sqlite:///:memory:',
        'WHISPER_MODEL_SIZE': 'base',
        'LLM_MODEL_NAME': 'test_model',
        'OLLAMA_HOST': 'http://test:11434',
        'TTS_MODEL_NAME': 'test_tts_model',
        'SECRET_KEY': 'test_secret_key_for_testing',
        'AUDIO_DIR': os.path.join(backend_dir, 'test_audio')
    })
    
    return test_env

def main():
    """Run the tests."""
    print("🧪 Setting up test environment for Windows...")
    
    # Create test directories
    os.makedirs("tests", exist_ok=True)
    os.makedirs("tests/test_models", exist_ok=True)
    os.makedirs("tests/test_api", exist_ok=True)
    os.makedirs("test_audio", exist_ok=True)
    
    # Create __init__.py files
    for dir_path in ["tests", "tests/test_models", "tests/test_api"]:
        init_file = os.path.join(dir_path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("# Test package\n")
    
    test_env = setup_environment()
    
    print("🚀 Running tests...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "--tb=short"],
            env=test_env,
            check=True
        )
        print("✅ All tests passed!")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    sys.exit(main())