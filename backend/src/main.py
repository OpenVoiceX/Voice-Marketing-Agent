# backend/src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # <-- Import StaticFiles
from .core.config import settings # <-- Import settings
from .models import campaign as campaign_model
from .api.routes import agents, calls, campaigns as campaigns_router, chat
from .core.database import engine
from .models import agent as agent_model, call as call_model

agent_model.Base.metadata.create_all(bind=engine)
call_model.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="VoiceGenie API",
    description="API for managing real-time AI voice agents.",
    version="0.1.0",
)

# --- Mount a static directory to serve audio files ---
# This makes any file in settings.AUDIO_DIR available at the /audio URL
app.mount("/audio", StaticFiles(directory=settings.AUDIO_DIR), name="audio")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(calls.router, prefix="/api/v1/calls", tags=["Calls"])
app.include_router(campaigns_router.router, prefix="/api/v1/campaigns", tags=["Campaigns"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"]) 


@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Welcome to VoiceGenie API"}