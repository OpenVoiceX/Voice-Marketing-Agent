# backend/src/agents/appointment_setter/logic.py

from typing import List, Dict
from ..base_agent import BaseAgent
from .prompts import APPOINTMENT_SETTER_SYSTEM_PROMPT # <-- IMPORT THIS
from ...services.llm_service import LLMService

class AppointmentSetterAgent(BaseAgent):
    """A voice agent specialized in setting appointments."""

    # We now expect a system_prompt to be passed in.
    def __init__(self, llm_service: LLMService, system_prompt: str = APPOINTMENT_SETTER_SYSTEM_PROMPT):
        self.llm_service = llm_service
        self.system_prompt = system_prompt

    def get_initial_greeting(self) -> str:
        """
        Generate a dynamic initial greeting using the agent's system prompt.
        """
        # Use the LLM to generate a greeting based on the system prompt
        messages = [
            {"role": "system", "content": self.system_prompt + "\n\nIMPORTANT: Generate ONLY a brief 1-sentence greeting. Maximum 15 words."},
            {"role": "user", "content": "Start the conversation with a brief greeting."}
        ]
        
        greeting = self.llm_service.get_response(messages)
        return greeting

    def process_response(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Uses the LLM to generate a response based on the conversation.
        """
        # Add extra emphasis on brevity for voice interactions
        enhanced_prompt = self.system_prompt + "\n\n**CRITICAL FOR VOICE: Respond in MAXIMUM 2 short sentences (under 30 words total). No bullet points. No lists. Natural speech only.**"
        
        messages = [{"role": "system", "content": enhanced_prompt}]
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_input})
        
        ai_response = self.llm_service.get_response(messages)
        
        return ai_response