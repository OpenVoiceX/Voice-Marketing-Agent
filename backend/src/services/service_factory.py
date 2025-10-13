# backend/src/services/service_factory.py
"""
Service Factory for creating agent-specific service instances.
Allows each agent to use different LLM providers, TTS voices, and STT providers.
"""

from typing import Optional
from .llm_service import LLMService
from .tts_service import TTSService
from .stt_service import STTService
from ..models.agent import Agent
from ..core.config import settings


class ServiceFactory:
    """Factory for creating service instances with agent-specific configurations."""
    
    @staticmethod
    def create_llm_service(
        provider: Optional[str] = None,
        model: Optional[str] = None
    ) -> LLMService:
        """
        Create an LLM service with specified provider and model.
        
        Args:
            provider: LLM provider ('gemini' or 'groq'). Defaults to settings.LLM_PROVIDER
            model: Model name. Defaults based on provider
            
        Returns:
            Configured LLMService instance
        """
        if provider is None:
            provider = settings.LLM_PROVIDER
        if model is None:
            model = settings.GROQ_MODEL if provider == "groq" else settings.GEMINI_MODEL
            
        return LLMService(provider=provider, model=model)
    
    @staticmethod
    def create_tts_service(voice_id: Optional[str] = None) -> TTSService:
        """
        Create a TTS service with specified voice.
        
        Args:
            voice_id: ElevenLabs voice ID. Defaults to settings.ELEVENLABS_VOICE_ID
            
        Returns:
            Configured TTSService instance
        """
        if voice_id is None:
            voice_id = settings.ELEVENLABS_VOICE_ID
            
        return TTSService(voice_id=voice_id)
    
    @staticmethod
    def create_stt_service(provider: Optional[str] = None) -> STTService:
        """
        Create an STT service with specified provider.
        
        Args:
            provider: STT provider ('deepgram' or 'gemini'). Defaults to settings.STT_PROVIDER
            
        Returns:
            Configured STTService instance
        """
        if provider is None:
            provider = settings.STT_PROVIDER
            
        return STTService(provider=provider)
    
    @classmethod
    def create_services_for_agent(cls, agent: Agent) -> dict:
        """
        Create all services (LLM, TTS, STT) configured for a specific agent.
        
        Args:
            agent: Agent model instance with configuration
            
        Returns:
            Dictionary with 'llm', 'tts', 'stt' service instances
        """
        return {
            'llm': cls.create_llm_service(
                provider=agent.llm_provider,
                model=agent.llm_model
            ),
            'tts': cls.create_tts_service(
                voice_id=agent.tts_voice_id
            ),
            'stt': cls.create_stt_service(
                provider=agent.stt_provider
            )
        }


# Convenience instance for direct usage
service_factory = ServiceFactory()
