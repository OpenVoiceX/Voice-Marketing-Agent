# backend/src/api/routes/campaigns.py

# --- ALL NECESSARY IMPORTS ARE NOW INCLUDED ---
import csv
import io
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Response
from sqlalchemy.orm import Session, joinedload
# -----------------------------------------------

from ...core.database import get_db
from ...models import campaign as campaign_model
from ...schemas import campaign as campaign_schema
from ...services.campaign_service import campaign_service

router = APIRouter()

@router.post("/", response_model=campaign_schema.Campaign, status_code=status.HTTP_201_CREATED)
def create_campaign(campaign: campaign_schema.CampaignCreate, db: Session = Depends(get_db)):
    db_campaign = campaign_model.Campaign(name=campaign.name, agent_id=campaign.agent_id)
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@router.get("/", response_model=List[campaign_schema.Campaign])
def read_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Your joinedload optimization is included here. Great work!
    campaigns = db.query(campaign_model.Campaign).options(joinedload(campaign_model.Campaign.contacts)).offset(skip).limit(limit).all()
    return campaigns
    
@router.get("/{campaign_id}", response_model=campaign_schema.Campaign)
def read_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).options(joinedload(campaign_model.Campaign.contacts)).filter(campaign_model.Campaign.id == campaign_id).first()
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

@router.post("/{campaign_id}/contacts", status_code=status.HTTP_201_CREATED)
async def add_contacts_from_csv(campaign_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    contents = await file.read()
    file_like_object = io.StringIO(contents.decode())
    
    try:
        csv_reader = csv.DictReader(file_like_object)
        contacts_to_add = []
        header = [h.lower().strip() for h in csv_reader.fieldnames]
        if 'phone_number' not in header:
             raise HTTPException(status_code=400, detail="CSV file must contain a 'phone_number' header.")

        for row in csv_reader:
            phone_number = next((row[key] for key in row if key.lower().strip() == 'phone_number'), None)
            if phone_number:
                contacts_to_add.append(campaign_model.Contact(
                    phone_number=phone_number.strip(),
                    campaign_id=campaign_id
                ))
    except Exception:
        raise HTTPException(status_code=400, detail="Could not process CSV file. Please ensure it is a valid CSV with a 'phone_number' header.")
        
    if not contacts_to_add:
        raise HTTPException(status_code=400, detail="No valid phone numbers found in the 'phone_number' header.")
    
    db.add_all(contacts_to_add)
    db.commit()

    return {"message": f"{len(contacts_to_add)} contacts added to campaign {campaign_id}"}

@router.post("/{campaign_id}/start")
def start_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Check if campaign has contacts
    if not db_campaign.contacts:
        raise HTTPException(status_code=400, detail="Cannot start campaign: No contacts found. Please add contacts first.")
    
    try:
        # Use the campaign service to actually start making calls
        campaign_service.run_campaign(db, campaign_id)
        return {"message": f"Campaign {campaign_id} started successfully. Initiating calls to {len(db_campaign.contacts)} contacts."}
    except Exception as e:
        # If there's an error with Twilio or other services, still update the status
        db_campaign.status = "running"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Campaign started but encountered errors: {str(e)}")
    
@router.post("/{campaign_id}/stop")
def stop_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db_campaign.status = "paused"
    db.commit()
    return {"message": f"Campaign {campaign_id} stopped."}

@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = db.query(campaign_model.Campaign).filter(campaign_model.Campaign.id == campaign_id).first()
    if not db_campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    db.delete(db_campaign)
    db.commit()
    
    # --- CORRECTED RETURN STATEMENT ---
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # ----------------------------------