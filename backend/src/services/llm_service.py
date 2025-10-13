"""
LLM Service supporting both Gemini and Groq APIs for conversational AI.
"""
import google.generativeai as genai
from groq import Groq
from ..core.config import settings


class LLMService:
    """A service to interact with Gemini or Groq APIs for language model inference."""

    def __init__(self, provider: str = None, model: str = None):
        """
        Initialize LLM service with specified provider and model.
        
        Args:
            provider: LLM provider ('gemini' or 'groq'). Defaults to settings.LLM_PROVIDER
            model: Model name. Defaults based on provider
        """
        self.provider = (provider or settings.LLM_PROVIDER).lower()
        self.custom_model = model  # Store custom model if provided
        
        if self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "groq":
            self._init_groq()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}. Choose 'gemini' or 'groq'.")
    
    def _init_gemini(self):
        """Initialize Gemini API client."""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Use the simple model name without 'models/' prefix
            model_name = self.custom_model or settings.GEMINI_MODEL
            # Remove 'models/' prefix if present
            if model_name.startswith('models/'):
                model_name = model_name.replace('models/', '')
            
            # Map old/common model names to current Gemini model names
            model_mapping = {
                'gemini-1.5-flash': 'gemini-2.0-flash-exp',
                'gemini-1.5-flash-latest': 'gemini-2.0-flash-exp',
                'gemini-1.5-pro': 'gemini-2.0-flash-exp',
                'gemini-1.5-pro-latest': 'gemini-2.0-flash-exp',
                'gemini-pro': 'gemini-2.0-flash-exp',
            }
            
            # Use mapped name if available, otherwise use as-is
            actual_model = model_mapping.get(model_name, model_name)
            
            self.model = genai.GenerativeModel(actual_model)
            print(f"✅ LLMService: Successfully initialized Gemini with model '{actual_model}'.")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini: {e}")
            raise
    
    def _init_groq(self):
        """Initialize Groq API client."""
        try:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            self.model_name = self.custom_model or settings.GROQ_MODEL
            print(f"✅ LLMService: Successfully initialized Groq with model '{self.model_name}'.")
        except Exception as e:
            print(f"❌ Failed to initialize Groq: {e}")
            raise

    def get_response(self, messages):
        """
        Gets a chat completion from the configured LLM provider.
        
        Args:
            messages: List of message dicts with 'role' and 'content' keys
                     (OpenAI chat format: [{role: 'user', content: '...'}, ...])
        
        Returns:
            str: The model's response text
        """
        try:
            if self.provider == "gemini":
                return self._get_gemini_response(messages)
            elif self.provider == "groq":
                return self._get_groq_response(messages)
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            return "I'm sorry, I'm having trouble thinking right now."
    
    def _get_gemini_response(self, messages):
        """Get response from Gemini API."""
        # Convert OpenAI format to Gemini format
        # Gemini uses a chat session with history
        chat = self.model.start_chat(history=[])
        
        # Build conversation history
        for msg in messages[:-1]:  # All but last message
            role = "user" if msg["role"] == "user" else "model"
            chat.history.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        # Send the last message and get response
        last_message = messages[-1]["content"]
        response = chat.send_message(
            last_message,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=60,  # Very short responses for voice chat (40-50 words max)
                temperature=0.7,
            )
        )
        return response.text
    
    def _get_groq_response(self, messages):
        """Get response from Groq API."""
        # Groq uses OpenAI-compatible format
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=60,  # Very short responses for voice chat (40-50 words max)
        )
        return response.choices[0].message.content
