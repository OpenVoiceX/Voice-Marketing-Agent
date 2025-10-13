# backend/src/services/campaign_service.py
import asyncio
import threading
import time
import os
from sqlalchemy.orm import Session
from ..models import campaign as campaign_model
from ..schemas import campaign as campaign_schema
from .telephony_service import twilio_service
from .service_factory import service_factory

class CampaignService:
    def __init__(self):
        # Check if we're in test mode (for development)
        self.test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
        if self.test_mode:
            print("🧪 Running in TEST MODE - calls will be simulated")
        else:
            print("🚀 Running in LIVE MODE - real calls will be made")

    def run_campaign(self, db: Session, campaign_id: int):
        """
        Start a campaign by initiating calls to all contacts.
        This runs in a separate thread to avoid blocking the API response.
        """
        campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
        if not campaign:
            raise Exception("Campaign not found")

        # Update campaign status to running
        campaign.status = "running"
        db.commit()

        # Start calling in a separate thread to avoid blocking
        thread = threading.Thread(target=self._make_calls_sequentially, args=(campaign_id,))
        thread.daemon = True
        thread.start()

        mode_text = "TEST MODE (simulated)" if self.test_mode else "LIVE MODE"
        return {"message": f"Campaign {campaign_id} started in {mode_text}. Initiating calls to {len(campaign.contacts)} contacts sequentially."}

    def _make_calls_sequentially(self, campaign_id: int):
        """
        Internal method to make calls to all contacts in a campaign sequentially.
        This runs in a separate thread and calls contacts one by one with delays.
        Uses agent-specific service configurations for each campaign.
        """
        from ..core.database import SessionLocal
        from ..models import agent as agent_model
        
        db = SessionLocal()
        try:
            campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
            if not campaign:
                print(f"Campaign {campaign_id} not found in _make_calls_sequentially")
                return

            # Get agent configuration for this campaign
            agent = db.query(agent_model.Agent).filter(agent_model.Agent.id == campaign.agent_id).first()
            if not agent:
                print(f"❌ Agent {campaign.agent_id} not found for campaign {campaign_id}")
                return
            
            print(f"Starting sequential calls to {len(campaign.contacts)} contacts for campaign {campaign_id}")
            print(f"Mode: {'TEST (simulated)' if self.test_mode else 'LIVE'}")
            print(f"🔧 Agent Configuration:")
            print(f"   LLM: {agent.llm_provider} ({agent.llm_model})")
            print(f"   TTS Voice: {agent.tts_voice_id}")
            print(f"   STT: {agent.stt_provider}")
            
            for i, contact in enumerate(campaign.contacts):
                try:
                    print(f"Calling contact {i+1}/{len(campaign.contacts)}: {contact.phone_number}")
                    
                    # Update contact status to calling
                    contact.status = "calling"
                    db.commit()
                    
                    if self.test_mode:
                        # TEST MODE: Simulate successful calls
                        print(f"🧪 TEST MODE: Simulating call to {contact.phone_number}")
                        time.sleep(3)  # Simulate call processing time
                        
                        # Simulate 80% success rate for testing
                        import random
                        if random.random() < 0.8:
                            contact.status = "completed"
                            print(f"✅ TEST MODE: Call completed successfully for {contact.phone_number}")
                        else:
                            contact.status = "failed"
                            print(f"❌ TEST MODE: Call failed for {contact.phone_number}")
                        
                        db.commit()
                    else:
                        # LIVE MODE: Make actual Twilio calls with agent-specific settings
                        try:
                            result = twilio_service.originate_call(
                                to_number=contact.phone_number, 
                                agent_id=campaign.agent_id  # Twilio will use agent config via webhook
                            )
                            print(f"📞 LIVE MODE: Call initiated for {contact.phone_number} with agent config")
                            print(f"   Using: {agent.llm_provider}/{agent.llm_model}, Voice: {agent.tts_voice_id[:8]}..., STT: {agent.stt_provider}")
                        except Exception as e:
                            print(f"❌ LIVE MODE: Failed to call {contact.phone_number}: {e}")
                            contact.status = "failed"
                            db.commit()
                    
                    # Wait between calls to ensure sequential calling
                    if i < len(campaign.contacts) - 1:  # Don't wait after the last call
                        wait_time = 5 if self.test_mode else 10  # Shorter wait in test mode
                        print(f"⏳ Waiting {wait_time} seconds before next call...")
                        time.sleep(wait_time)
                    
                except Exception as e:
                    print(f"❌ Error processing call for {contact.phone_number}: {e}")
                    contact.status = "failed"
                    db.commit()
                    
                    # Still wait before next call even if this one failed
                    if i < len(campaign.contacts) - 1:
                        wait_time = 5 if self.test_mode else 10
                        print(f"⏳ Waiting {wait_time} seconds before next call...")
                        time.sleep(wait_time)
                    
        except Exception as e:
            print(f"Error in _make_calls_sequentially for campaign {campaign_id}: {e}")
        finally:
            db.close()

    def get_campaign_status(self, db: Session, campaign_id: int):
        """
        Get detailed status of a campaign including contact call statuses.
        """
        campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
        if not campaign:
            raise Exception("Campaign not found")
        
        # Count contacts by status
        status_counts = {}
        for contact in campaign.contacts:
            status = contact.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "campaign_id": campaign_id,
            "campaign_status": campaign.status,
            "total_contacts": len(campaign.contacts),
            "status_breakdown": status_counts,
            "mode": "TEST" if self.test_mode else "LIVE"
        }

campaign_service = CampaignService()
