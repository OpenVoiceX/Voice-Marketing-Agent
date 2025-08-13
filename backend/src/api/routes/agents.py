# backend/src/api/routes/agents.py

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models import agent as agent_model
from ...schemas import agent as agent_schema
import logging

router = APIRouter()

@router.post("/", response_model=agent_schema.Agent, status_code=status.HTTP_201_CREATED)
def create_agent(agent: agent_schema.AgentCreate, db: Session = Depends(get_db)):
    """
    Create a new voice agent.
    """
    db_agent = agent_model.Agent(
        name=agent.name,
        system_prompt=agent.system_prompt,
        voice_id=agent.voice_id
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    logging.INFO("A new agent has been created")
    return db_agent

@router.get("/{agent_id}", response_model=agent_schema.Agent)
def read_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific agent by its ID.
    """
    db_agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == agent_id).first()
    if db_agent is None:
        logging.ERROR("Agent not found")
        raise HTTPException(status_code=404, detail="Agent not found")
    logging.INFO(f"agent with the {agent_id} has been retrieved")
    return db_agent

@router.get("/", response_model=List[agent_schema.Agent])
def read_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of all agents.
    """
    agents = db.query(agent_model.Agent).offset(skip).limit(limit).all()
    return agents