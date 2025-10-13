# backend/src/api/routes/chat.py

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import json
import asyncio

from ...core.database import get_db
from ...models import agent as agent_model
from ...services.service_factory import service_factory
from ...agents.appointment_setter.logic import AppointmentSetterAgent

router = APIRouter()

# Store active chat sessions
chat_sessions = {}

class ChatMessage(BaseModel):
    agent_id: int
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    agent_id: int
    user_message: str
    agent_response: str
    session_id: str

@router.post("/text", response_model=ChatResponse)
async def chat_with_agent(chat_msg: ChatMessage, db: Session = Depends(get_db)):
    """
    Simple text chat with an agent. Send a message, get a response.
    """
    # Get agent from database
    agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == chat_msg.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID {chat_msg.agent_id} not found")
    
    # Create only LLM service for text chat (no need for TTS/STT)
    llm_service = service_factory.create_llm_service(
        provider=agent.llm_provider or 'gemini',
        model=agent.llm_model or 'gemini-1.5-flash'
    )
    
    # Initialize the appointment setter agent
    ai_agent = AppointmentSetterAgent(llm_service=llm_service, system_prompt=agent.system_prompt)
    
    # Get or create conversation history for this session
    session_key = f"{chat_msg.agent_id}_{chat_msg.session_id}"
    if session_key not in chat_sessions:
        chat_sessions[session_key] = []
    
    conversation_history = chat_sessions[session_key]
    
    # Get AI response
    ai_response = ai_agent.process_response(chat_msg.message, conversation_history)
    
    # Update conversation history with proper format
    conversation_history.append({"role": "user", "content": chat_msg.message})
    conversation_history.append({"role": "assistant", "content": ai_response})
    chat_sessions[session_key] = conversation_history[-20:]  # Keep last 20 messages (10 exchanges)
    
    return ChatResponse(
        agent_id=chat_msg.agent_id,
        user_message=chat_msg.message,
        agent_response=ai_response,
        session_id=chat_msg.session_id
    )

@router.websocket("/voice/{agent_id}")
async def voice_chat_websocket(websocket: WebSocket, agent_id: int, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for real-time voice chat with an agent.
    Receives text from browser (already transcribed by browser), returns text response.
    Browser handles TTS playback using Web Speech API.
    """
    await websocket.accept()
    
    try:
        # Get agent from database
        agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == agent_id).first()
        if not agent:
            await websocket.send_json({"error": f"Agent with ID {agent_id} not found"})
            await websocket.close()
            return
        
        # Create only LLM service for voice chat (browser handles STT/TTS)
        llm_service = service_factory.create_llm_service(
            provider=agent.llm_provider or 'gemini',
            model=agent.llm_model or 'gemini-1.5-flash'
        )
        
        # Initialize the appointment setter agent
        ai_agent = AppointmentSetterAgent(llm_service=llm_service, system_prompt=agent.system_prompt)
        
        conversation_history = []
        
        # Send initial greeting
        greeting = ai_agent.get_initial_greeting()
        
        await websocket.send_json({
            "type": "agent_response",
            "text": greeting
        })
        
        # Listen for user messages
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "user_text":
                # User sent text message (already transcribed by browser)
                user_text = data.get("text", "")
                
                if not user_text.strip():
                    continue
                
                # Get AI response
                ai_response_text = ai_agent.process_response(user_text, conversation_history)
                
                # Send response back (browser will speak it)
                await websocket.send_json({
                    "type": "agent_response",
                    "text": ai_response_text
                })
                
                # Update conversation history
                conversation_history.append({"role": "user", "content": user_text})
                conversation_history.append({"role": "assistant", "content": ai_response_text})
                conversation_history = conversation_history[-20:]  # Keep last 20 messages
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for agent {agent_id}")
    except Exception as e:
        print(f"Error in voice chat WebSocket: {e}")
        await websocket.send_json({"error": str(e)})
        await websocket.close()

@router.delete("/session/{agent_id}/{session_id}")
async def clear_chat_session(agent_id: int, session_id: str):
    """
    Clear a chat session history.
    """
    session_key = f"{agent_id}_{session_id}"
    if session_key in chat_sessions:
        del chat_sessions[session_key]
        return {"message": f"Session {session_id} cleared for agent {agent_id}"}
    return {"message": "Session not found"}

@router.get("/sessions/{agent_id}")
async def get_chat_sessions(agent_id: int):
    """
    Get all active sessions for an agent.
    """
    sessions = []
    for key in chat_sessions.keys():
        if key.startswith(f"{agent_id}_"):
            session_id = key.split("_", 1)[1]
            sessions.append({
                "session_id": session_id,
                "message_count": len(chat_sessions[key])
            })
    return {"agent_id": agent_id, "sessions": sessions}
