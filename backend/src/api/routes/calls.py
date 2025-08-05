# backend/src/api/routes/calls.py

import os
import uuid
import traceback # Import for detailed error logging
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, Query
from fastapi.responses import Response # Import Response for returning XML
from sqlalchemy.orm import Session
from pydantic import BaseModel

# --- IMPORT TWILIO'S TwiML BUILDER ---
from twilio.twiml.voice_response import VoiceResponse, Gather
# -------------------------------------

from ...core.database import get_db
from ...services.llm_service import LLMService
from ...services.stt_service import STTService
from ...services.tts_service import TTSService
from ...services.telephony_service import twilio_service
from ...agents.appointment_setter.logic import AppointmentSetterAgent
from ...models import agent as agent_model, campaign as campaign_model

router = APIRouter()

# Service Initialization
stt_service = STTService()
tts_service = TTSService()
llm_service = LLMService()

class OriginateCallRequest(BaseModel):
    to_number: str
    agent_id: int

@router.post("/originate")
def originate_call(request: OriginateCallRequest, db: Session = Depends(get_db)):
    db_agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == request.agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail=f"Agent with ID {request.agent_id} not found.")

    try:
        result = twilio_service.originate_call(
            to_number=request.to_number,
            agent_id=request.agent_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate call. Error: {str(e)}")


@router.post("/webhook", response_class=Response(media_type="application/xml"))
async def call_webhook(
    db: Session = Depends(get_db),
    agent_id: int = Query(...),
    # Twilio sends speech recognition results in the 'SpeechResult' field
    SpeechResult: str = Form(None), 
    # Twilio sends the Call SID with a capital 'S'
    CallSid: str = Form(...),
    # Twilio sends call status updates
    CallStatus: str = Form(None),
    To: str = Form(None)
):
    """
    Main webhook to handle call progression. Now returns proper TwiML.
    """
    print(f"--- WEBHOOK TRIGGERED for CallSid: {CallSid} ---")
    print(f"Call Status: {CallStatus}, To: {To}")
    response = VoiceResponse()

    try:
        # Update contact status based on call status
        if To and CallStatus:
            contact = db.query(campaign_model.Contact).filter(
                campaign_model.Contact.phone_number == To
            ).first()
            
            if contact:
                if CallStatus in ['completed', 'answered']:
                    contact.status = 'completed'
                elif CallStatus in ['failed', 'busy', 'no-answer']:
                    contact.status = 'failed'
                elif CallStatus == 'in-progress':
                    contact.status = 'calling'
                db.commit()
                print(f"Updated contact {To} status to {contact.status}")

        db_agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == agent_id).first()
        if not db_agent:
            print(f"❌ ERROR: Agent with ID {agent_id} not found in webhook.")
            response.say("Sorry, an internal error occurred. Goodbye.")
            response.hangup()
            return Response(content=str(response), media_type="application/xml")

        agent = AppointmentSetterAgent(llm_service=llm_service, system_prompt=db_agent.system_prompt)
        
        conversation_history = [] # In a real app, you'd store and retrieve this from the DB based on CallSid

        if SpeechResult is None:
            # This is the first webhook hit (user just answered)
            print("🎙️ No speech result, generating initial greeting...")
            greeting_text = agent.get_initial_greeting()
            response.say(greeting_text)
            
            # Tell Twilio to listen for the user's response and call this webhook back
            gather = Gather(input='speech', action=f'/api/v1/calls/webhook?agent_id={agent_id}', speechTimeout='auto')
            response.append(gather)
            print("✅ Responded with greeting and gather instruction.")

        else:
            # The user has spoken, and Twilio has transcribed it
            user_transcript = SpeechResult
            print(f"🎤 User said: '{user_transcript}'")

            ai_response_text = agent.process_response(user_transcript, conversation_history)
            print(f"🤖 AI will say: '{ai_response_text}'")

            response.say(ai_response_text)
            
            if "goodbye" in ai_response_text.lower():
                print("🏁 AI said goodbye, responding with Hangup.")
                response.hangup()
            else:
                print("👂 Responding with Say and gathering next user input...")
                gather = Gather(input='speech', action=f'/api/v1/calls/webhook?agent_id={agent_id}', speechTimeout='auto')
                response.append(gather)

        final_twiml = str(response)
        print(f"➡️  Responding to Twilio with TwiML:\n{final_twiml}")
        return Response(content=final_twiml, media_type="application/xml")

    except Exception as e:
        print(f"🔥🔥🔥 UNEXPECTED ERROR IN WEBHOOK 🔥🔥🔥")
        print(f"Error: {e}")
        traceback.print_exc()
        
        # Respond with a safe error message to Twilio
        error_response = VoiceResponse()
        error_response.say("I'm sorry, an unexpected error has occurred. Goodbye.")
        error_response.hangup()
        return Response(content=str(error_response), media_type="application/xml")