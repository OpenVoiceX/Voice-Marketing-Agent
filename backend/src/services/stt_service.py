from faster_whisper import WhisperModel
from ..core.config import settings

class STTService:
    """A service for Speech-to-Text using the optimized Faster-Whisper library."""

    def __init__(self):
        try:
            # FIXED: Corrected the typo from WISPHER_MODEL_SIZE to WHISPER_MODEL_SIZE
            model_size = settings.WHISPER_MODEL_SIZE
            compute_type = "int8"  # Use INT8 quantization for speed
            
            print(f"Initializing Faster-Whisper with model: {model_size}")
            print(f"Using compute type: {compute_type} on CPU")

            # Load the model onto the CPU with INT8 quantization for speed
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
            # The transcribe method returns an iterator of segment objects
            segments, info = self.model.transcribe(audio_file_path, beam_size=5)
            
            print(f"Detected language '{info.language}' with probability {info.language_probability}")

            # Concatenate the text from all segments
            full_transcript = "".join(segment.text for segment in segments)
            
            return full_transcript.strip()
            
        except Exception as e:
            print(f"Error during transcription with Faster-Whisper: {e}")
            return "" # Return empty string on error