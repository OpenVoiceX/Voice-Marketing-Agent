# backend/src/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'  # Ignore extra fields in .env file
    )

    # Database
    DATABASE_URL: str

    # AI Services - Cloud APIs
    # Gemini Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"  # Default model
    
    # Groq Configuration
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.1-70b-versatile"  # Default model
    
    # LLM Provider Selection (gemini or groq)
    LLM_PROVIDER: str = "gemini"
    
    # ElevenLabs Configuration
    ELEVENLABS_API_KEY: str
    ELEVENLABS_VOICE_ID: str = "21m00Tcm4TlvDq8ikWAM"  # Default voice (Rachel)
    ELEVENLABS_MODEL_ID: str = "eleven_monolingual_v1"
    
    # STT Configuration
    # Gemini Voice API for STT
    GEMINI_VOICE_MODEL: str = "gemini-1.5-flash"
    
    # Deepgram Configuration
    DEEPGRAM_AUTH_TOKEN: str
    DEEPGRAM_MODEL: str = "nova-2"  # Options: nova-2, nova, enhanced, base
    
    # STT Provider Selection (gemini or deepgram)
    STT_PROVIDER: str = "deepgram"

    # Telephony (Twilio)
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    TWILIO_WEBHOOK_URL: str = ""  # Optional webhook URL
    
    # App
    SECRET_KEY: str
    AUDIO_DIR: str
    PUBLIC_URL: str
    TEST_MODE: str = "false"  # Set to "true" to simulate calls without Twilio

settings = Settings()