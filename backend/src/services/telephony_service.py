# backend/src/services/telephony_service.py
from twilio.rest import Client
from ..core.config import settings
import logging

class TwilioService:
    _client = None

    @classmethod
    def get_client(cls):
        """
        Returns a singleton instance of the Twilio client.
        Initializes the client on first call and validates credentials.
        """
        if cls._client is None:
            # Check if the environment variables are loaded and not empty
            if not all([
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN,
                settings.TWILIO_PHONE_NUMBER
            ]):
                raise ValueError("Server is not configured for making calls. TWILIO environment variables are missing or empty.")
            
            try:
                logging.INFO("Initializing Twilio client...")
                cls._client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                logging.INFO("✅ Twilio client initialized successfully.")
            except Exception as e:
                logging.ERROR(f"❌ Failed to initialize Twilio client: {e}")
                raise ConnectionError(f"Failed to initialize Twilio client. Check credentials. Error: {e}")
        
        return cls._client

    def originate_call(self, to_number: str, agent_id: int):
        """
        Originates a new call using Twilio.
        """
        client = self.get_client()
        
        # IMPORTANT: For Twilio webhooks to work, your server must be publicly accessible.
        # During local development, you must use a tool like ngrok to expose your localhost:8000.
        # Replace 'http://your_ngrok_or_public_url.io' with your actual ngrok URL.
        public_url = settings.PUBLIC_URL 
        
        try:
            logging.INFO(f"Attempting to call {to_number} from {settings.TWILIO_PHONE_NUMBER}...")
            call = client.calls.create(
                to=to_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                # This is the URL Twilio will call back to our webhook when the user answers.
                url=f"{public_url}/api/v1/calls/webhook?agent_id={agent_id}"
            )
            logging.INFO(f"Successfully initiated call with SID: {call.sid}")
            return {"status": "success", "call_sid": call.sid}
        except Exception as e:
            logging.ERROR(f"❌ Twilio call creation failed: {e}")
            # This will cause a 500 error, but the log will show the *real* reason
            # from Twilio (e.g., "The 'To' number is not a valid phone number").
            raise e

# Create a single instance of the service to be imported elsewhere
twilio_service = TwilioService()