# backend/src/utils/logging.py
import logging
import sys

# Configure a basic logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def log_call_event(call_sid: str, event: str, details: dict = None, level: str = "info"):
    """
    A structured logger for call events.

    Args:
        call_sid (str): Unique ID for a specific call when there is a call to the webhook endpoint from Twilio.
        event (str): Short and machine-readable name for what event just happened.
        details (dict, optional): Data payload for the event, containing actual information.
        level (str, optional): Logging level such as "info", "error", "debug". Defaults to "info".
    """
    message = f"CALL_EVENT: [SID: {call_sid}] [Event: {event}]"
    if details:
        message += f" [Details: {details}]"

    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message)
