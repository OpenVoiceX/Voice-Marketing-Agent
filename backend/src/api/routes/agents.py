# backend/src/api/routes/agents.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models import agent as agent_model
from ...schemas import agent as agent_schema

router = APIRouter()

@router.post("/", response_model=agent_schema.Agent, status_code=status.HTTP_201_CREATED)
def create_agent(agent: agent_schema.AgentCreate, db: Session = Depends(get_db)):
    """
    Create a new voice agent with configurable LLM, TTS, and STT providers.
    """
    db_agent = agent_model.Agent(
        name=agent.name,
        system_prompt=agent.system_prompt,
        voice_id=agent.voice_id,
        llm_provider=agent.llm_provider,
        llm_model=agent.llm_model,
        tts_voice_id=agent.tts_voice_id,
        stt_provider=agent.stt_provider
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.get("/{agent_id}", response_model=agent_schema.Agent)
def read_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific agent by its ID.
    """
    db_agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == agent_id).first()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent

@router.get("/", response_model=List[agent_schema.Agent])
def read_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all agents.
    """
    agents = db.query(agent_model.Agent).offset(skip).limit(limit).all()
    return agents


@router.get("/options/config")
def get_agent_options():
    """
    Get available options for agent configuration (LLM providers, voices, STT providers).
    This endpoint returns all available options for creating/editing agents.
    """
    return {
        "llm_providers": [
            {
                "id": "gemini",
                "name": "Google Gemini",
                "models": [
                    {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash (Fastest)"},
                    {"id": "gemini-1.5-pro", "name": "Gemini 1.5 Pro (Most Capable)"},
                    {"id": "gemini-1.0-pro", "name": "Gemini 1.0 Pro"}
                ]
            },
            {
                "id": "groq",
                "name": "Groq (Ultra-Fast)",
                "models": [
                    {"id": "llama-3.1-70b-versatile", "name": "Llama 3.1 70B (Recommended)"},
                    {"id": "llama-3.1-8b-instant", "name": "Llama 3.1 8B (Fastest)"},
                    {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B"}
                ]
            }
        ],
        "stt_providers": [
            {
                "id": "deepgram",
                "name": "Deepgram (Recommended)",
                "description": "Industry-leading STT with best accuracy and speed"
            },
            {
                "id": "gemini",
                "name": "Google Gemini",
                "description": "Multimodal AI with good STT capabilities"
            }
        ],
        "tts_voices": [
            {"id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel - Natural Female"},
            {"id": "AZnzlk1XvdvUeBnXmlld", "name": "Domi - Confident Female"},
            {"id": "EXAVITQu4vr4xnSDxMaL", "name": "Bella - Soft Female"},
            {"id": "ErXwobaYiN019PkySvjV", "name": "Antoni - Well-Rounded Male"},
            {"id": "MF3mGyEYCl7XYWbV9V6O", "name": "Elli - Emotional Female"},
            {"id": "TxGEqnHWrfWFTfGW9XjX", "name": "Josh - Deep Male"},
            {"id": "VR6AewLTigWG4xSOukaG", "name": "Arnold - Crisp Male"},
            {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam - Narrative Male"},
            {"id": "yoZ06aMxZJJ28mfd3POQ", "name": "Sam - Raspy Male"},
            {"id": "onwK4e9ZLuTAKqWW03F9", "name": "Daniel - Authoritative Male"}
        ]
    }