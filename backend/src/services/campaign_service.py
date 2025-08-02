# backend/src/services/campaign_service.py
from sqlalchemy.orm import Session
from .. import models, schemas
from .telephony_service import twilio_service

class CampaignService:
    def run_campaign(self, db: Session, campaign_id: int):
        campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
        if not campaign:
            raise Exception("Campaign not found")

        campaign.status = "running"
        db.commit()

        for contact in campaign.contacts:
            try:
                twilio_service.originate_call(to_number=contact.phone_number, agent_id=campaign.agent_id)
                contact.status = "calling"
            except Exception as e:
                print(f"Failed to call {contact.phone_number}: {e}")
                contact.status = "failed"
            db.commit()

campaign_service = CampaignService()
