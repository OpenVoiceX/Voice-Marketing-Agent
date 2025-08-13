# backend/src/services/campaign_service.py
import asyncio
import threading
import time
import os
from sqlalchemy.orm import Session
from ..models import campaign as campaign_model
from ..schemas import campaign as campaign_schema
from .telephony_service import twilio_service
import logging

class CampaignService:
    def __init__(self):
        # Check if we're in test mode (for development)
        self.test_mode = os.getenv('TEST_MODE', 'true').lower() == 'true'
        if self.test_mode:
            logging.INFO("🧪 Running in TEST MODE - calls will be simulated")

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
        """
        from ..core.database import SessionLocal
        
        db = SessionLocal()
        try:
            campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
            if not campaign:
                logging.INFO(f"Campaign {campaign_id} not found in _make_calls_sequentially")
                return

            logging.INFO(f"Starting sequential calls to {len(campaign.contacts)} contacts for campaign {campaign_id}")
            logging.INFO(f"Mode: {'TEST (simulated)' if self.test_mode else 'LIVE'}")
            
            for i, contact in enumerate(campaign.contacts):
                try:
                    logging(f"Calling contact {i+1}/{len(campaign.contacts)}: {contact.phone_number}")
                    
                    # Update contact status to calling
                    contact.status = "calling"
                    db.commit()
                    
                    if self.test_mode:
                        # TEST MODE: Simulate successful calls
                        logging.INFO(f"🧪 TEST MODE: Simulating call to {contact.phone_number}")
                        time.sleep(3)  # Simulate call processing time
                        
                        # Simulate 80% success rate for testing
                        import random
                        if random.random() < 0.8:
                            contact.status = "completed"
                            logging.INFO(f"✅ TEST MODE: Call completed successfully for {contact.phone_number}")
                        else:
                            contact.status = "failed"
                            logging.ERROR(f"❌ TEST MODE: Call failed for {contact.phone_number}")
                        
                        db.commit()
                    else:
                        # LIVE MODE: Make actual Twilio calls
                        try:
                            result = twilio_service.originate_call(
                                to_number=contact.phone_number, 
                                agent_id=campaign.agent_id
                            )
                            logging.INFO(f"📞 LIVE MODE: Call initiated for {contact.phone_number}: {result}")
                        except Exception as e:
                            logging.ERROR(f"❌ LIVE MODE: Failed to call {contact.phone_number}: {e}")
                            contact.status = "failed"
                            db.commit()
                    
                    # Wait between calls to ensure sequential calling
                    if i < len(campaign.contacts) - 1:  # Don't wait after the last call
                        wait_time = 5 if self.test_mode else 10  # Shorter wait in test mode
                        logging.INFO(f"⏳ Waiting {wait_time} seconds before next call...")
                        time.sleep(wait_time)
                    
                except Exception as e:
                    logging.ERROR(f"❌ Error processing call for {contact.phone_number}: {e}")
                    contact.status = "failed"
                    db.commit()
                    
                    # Still wait before next call even if this one failed
                    if i < len(campaign.contacts) - 1:
                        wait_time = 5 if self.test_mode else 10
                        logging.INFO(f"⏳ Waiting {wait_time} seconds before next call...")
                        time.sleep(wait_time)
                    
        except Exception as e:
            logging.ERROR(f"Error in _make_calls_sequentially for campaign {campaign_id}: {e}")
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
