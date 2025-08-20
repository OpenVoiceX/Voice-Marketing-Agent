# backend/src/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    DATABASE_URL: str

    # AI Services
    OLLAMA_HOST: str
    LLM_MODEL_NAME: str
    FASTER_WHISPER_MODEL_SIZE: str
    FASTER_WHISPER_COMPUTE_TYPE: str
    TTS_MODEL_NAME: str

    # Telephony (Twilio)
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    # App
    SECRET_KEY: str
    AUDIO_DIR: str
    PUBLIC_URL: str   # ✅ added earlier

    # Misc
    TEST_MODE: bool = False   # ✅ new line

settings = Settings()
