# backend/src/schemas/agent.py
from pydantic import BaseModel

class AgentBase(BaseModel):
    name: str
    system_prompt: str
    voice_id: str | None = None

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: int
    # NEW FIELD: Include last_call_status in the response
    last_call_status: str | None = "idle"

    class Config:
        from_attributes = True # Pydantic v2 name for orm_mode