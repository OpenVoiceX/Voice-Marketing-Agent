"""
Test utilities and helper functions for the test suite.
"""
import tempfile
import wave
import os


def create_test_wav_file(duration_seconds=1, sample_rate=16000):
    """
    Create a temporary WAV file for testing audio processing.
    
    Returns:
        str: Path to the created temporary file
    """
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.close()
    
    # Create a simple sine wave
    with wave.open(temp_file.name, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        
        # Generate simple audio data (silence for testing)
        frames = sample_rate * duration_seconds
        for _ in range(frames):
            wf.writeframesraw(b'\x00\x00')
    
    return temp_file.name


def cleanup_test_file(file_path):
    """Clean up a temporary test file."""
    try:
        os.unlink(file_path)
    except FileNotFoundError:
        pass