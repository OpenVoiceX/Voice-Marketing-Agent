# backend/src/services/tts_service.py
from TTS.api import TTS
from ..core.config import settings
import logging

class TTSService:
    """
    A service for Text-to-Speech using the Coqui TTS engine,
    which powers models like VITS (a good proxy for Kokoro-like speed).
    """

    def __init__(self):
        try:
            model_name = settings.TTS_MODEL_NAME
            logging.INFO(f"Initializing Coqui TTS engine with model: {model_name}")
            
            # Initialize TTS with the specified model, forcing it to run on CPU
            self.tts = TTS(model_name, gpu=False)

            logging.INFO("TTS service initialized successfully.")
        except Exception as e:
            logging.ERROR(f"Error initializing Coqui TTS: {e}")
            logging.ERROR("This might be the first run, and the model needs to be downloaded.")
            raise

    def synthesize(self, text: str, output_path: str):
        """Synthesizes text and saves it to an audio file."""
        try:
            # tts_to_file is a blocking call that saves the audio.
            self.tts.tts_to_file(text=text, file_path=output_path)
            logging.INFO(f"Synthesized audio with Coqui TTS and saved to {output_path}")
        except Exception as e:
            logging.ERROR(f"Error during Coqui TTS synthesis: {e}")