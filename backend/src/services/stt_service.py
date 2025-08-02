# backend/src/services/stt_service.py
from faster_whisper import WhisperModel
from ..core.config import settings

class STTService:
    """A service for Speech-to-Text using the optimized Faster-Whisper library."""

    def __init__(self):
        try:
            model_size = settings.FASTER_WHISPER_MODEL_SIZE
            compute_type = settings.FASTER_WHISPER_COMPUTE_TYPE
            
            print(f"Initializing Faster-Whisper with model: {model_size}")
            print(f"Using compute type: {compute_type} on CPU")

            # Load the model onto the CPU with INT8 quantization for speed.
            # 1. Indentation is now correct.
            # 2. Changed 'device=settings.WHISPER_DEVICE' to the correct 'device="cpu"'.
            self.model = WhisperModel(
                model_size, 
                device="cpu", 
                compute_type=compute_type
            )
            print("STTService initialized with Faster-Whisper.")
        except Exception as e:
            print(f"Error loading Faster-Whisper model: {e}")
            raise

    def transcribe(self, audio_file_path: str) -> str:
        """Transcribes audio from a file path."""
        try:
            segments, info = self.model.transcribe(audio_file_path, beam_size=5)
            
            print(f"Detected language '{info.language}' with probability {info.language_probability}")

            full_transcript = "".join(segment.text for segment in segments)
            
            return full_transcript.strip()
            
        except Exception as e:
            print(f"Error during transcription with Faster-Whisper: {e}")
            return ""