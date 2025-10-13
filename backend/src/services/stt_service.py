"""
STT Service supporting both Gemini and Deepgram APIs for audio transcription.
"""
import google.generativeai as genai
from deepgram import DeepgramClient
from ..core.config import settings


class STTService:
    """A service for Speech-to-Text using Gemini or Deepgram APIs."""

    def __init__(self, provider: str = None):
        """
        Initialize STT service with specified provider.
        
        Args:
            provider: STT provider ('deepgram' or 'gemini'). Defaults to settings.STT_PROVIDER
        """
        self.provider = (provider or settings.STT_PROVIDER).lower()
        
        if self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "deepgram":
            self._init_deepgram()
        else:
            raise ValueError(f"Unsupported STT provider: {self.provider}. Choose 'gemini' or 'deepgram'.")

    def _init_gemini(self):
        """Initialize Gemini STT API client."""
        try:
            print(f"Initializing Gemini STT service...")
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_VOICE_MODEL)
            print("✅ STTService initialized with Gemini API.")
        except Exception as e:
            print(f"❌ Error loading Gemini STT service: {e}")
            raise

    def _init_deepgram(self):
        """Initialize Deepgram API client."""
        try:
            print(f"Initializing Deepgram STT service...")
            self.client = DeepgramClient(settings.DEEPGRAM_AUTH_TOKEN)
            self.model = settings.DEEPGRAM_MODEL
            print(f"✅ STTService initialized with Deepgram API (model: {self.model}).")
        except Exception as e:
            print(f"❌ Error loading Deepgram STT service: {e}")
            raise

    def transcribe(self, audio_file_path: str) -> str:
        """
        Transcribes audio from a file path using the configured STT provider.
        
        Args:
            audio_file_path: Path to the audio file to transcribe
            
        Returns:
            str: Transcribed text from the audio
        """
        try:
            if self.provider == "gemini":
                return self._transcribe_gemini(audio_file_path)
            elif self.provider == "deepgram":
                return self._transcribe_deepgram(audio_file_path)
        except Exception as e:
            print(f"❌ Error during transcription: {e}")
            return ""

    def _transcribe_gemini(self, audio_file_path: str) -> str:
        """Transcribe using Gemini API."""
        try:
            # Upload the audio file
            print(f"Uploading audio file to Gemini: {audio_file_path}")
            audio_file = genai.upload_file(path=audio_file_path)
            
            # Create prompt for transcription
            prompt = "Please transcribe the speech in this audio file accurately. Only return the transcribed text without any additional comments or formatting."
            
            # Generate transcription
            response = self.model.generate_content([prompt, audio_file])
            
            # Clean up - delete the uploaded file
            audio_file.delete()
            
            transcribed_text = response.text.strip()
            print(f"✅ Gemini transcription completed: {transcribed_text[:50]}...")
            
            return transcribed_text
            
        except Exception as e:
            print(f"❌ Error during Gemini transcription: {e}")
            return ""

    def _transcribe_deepgram(self, audio_file_path: str) -> str:
        """Transcribe using Deepgram API."""
        try:
            print(f"Transcribing audio file with Deepgram: {audio_file_path}")
            
            # Read the audio file
            with open(audio_file_path, "rb") as audio:
                buffer_data = audio.read()

            # Configure Deepgram options
            options = {
                "model": self.model,
                "smart_format": True,
                "utterances": True,
                "punctuate": True,
                "diarize": False,
            }

            # Call the transcribe method with the audio buffer and options
            response = self.client.listen.prerecorded.v("1").transcribe_file(
                {"buffer": buffer_data},
                options
            )

            # Extract transcript from response
            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            
            print(f"✅ Deepgram transcription completed: {transcript[:50]}...")
            return transcript.strip()
            
        except Exception as e:
            print(f"❌ Error during Deepgram transcription: {e}")
            return ""
