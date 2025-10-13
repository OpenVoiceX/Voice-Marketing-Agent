# backend/src/models/agent.py
from sqlalchemy import Column, Integer, String, Text
from ..core.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    system_prompt = Column(Text, nullable=False)
    
    # LLM Configuration
    llm_provider = Column(String, default="gemini", nullable=False)  # gemini or groq
    llm_model = Column(String, default="gemini-1.5-flash", nullable=False)
    
    # TTS Configuration
    tts_voice_id = Column(String, default="21m00Tcm4TlvDq8ikWAM", nullable=False)  # ElevenLabs voice ID
    
    # STT Configuration
    stt_provider = Column(String, default="deepgram", nullable=False)  # deepgram or gemini
    
    # Legacy field (kept for backward compatibility)
    voice_id = Column(String, default="default_voice")