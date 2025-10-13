# backend/src/schemas/agent.py
from pydantic import BaseModel
from typing import Optional

class AgentBase(BaseModel):
    name: str
    system_prompt: str
    voice_id: Optional[str] = "default_voice"  # Legacy field
    
    # New configuration fields
    llm_provider: str = "gemini"  # gemini or groq
    llm_model: str = "gemini-1.5-flash"
    tts_voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # ElevenLabs voice ID
    stt_provider: str = "deepgram"  # deepgram or gemini

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int

    class Config:
        from_attributes = True # Pydantic v2 name for orm_mode