"""
TTS Service using ElevenLabs API for high-quality voice synthesis.
"""
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from ..core.config import settings


class TTSService:
    """
    A service for Text-to-Speech using the ElevenLabs API.
    Provides high-quality, natural-sounding voice synthesis.
    """

    def __init__(self, voice_id: str = None):
        """
        Initialize TTS service with specified voice.
        
        Args:
            voice_id: ElevenLabs voice ID. Defaults to settings.ELEVENLABS_VOICE_ID
        """
        try:
            print(f"Initializing ElevenLabs TTS service...")
            
            # Initialize ElevenLabs client with API key
            self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
            self.voice_id = voice_id or settings.ELEVENLABS_VOICE_ID
            self.model_id = settings.ELEVENLABS_MODEL_ID

            print(f"✅ TTS service initialized successfully with voice ID: {self.voice_id}")
        except Exception as e:
            print(f"❌ Error initializing ElevenLabs TTS: {e}")
            raise

    def synthesize(self, text: str, output_path: str):
        """
        Synthesizes text and saves it to an audio file using ElevenLabs API.
        
        Args:
            text: The text to convert to speech
            output_path: Path where the audio file will be saved
        """
        try:
            # Generate audio using ElevenLabs API
            audio_generator = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                model_id=self.model_id,
                text=text,
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.0,
                    use_speaker_boost=True
                )
            )
            
            # Save the audio to file
            with open(output_path, 'wb') as audio_file:
                for chunk in audio_generator:
                    audio_file.write(chunk)
            
            print(f"✅ Synthesized audio with ElevenLabs and saved to {output_path}")
            
        except Exception as e:
            print(f"❌ Error during ElevenLabs TTS synthesis: {e}")
            raise
