# backend/src/schemas/campaign.py
from pydantic import BaseModel
from typing import List, Optional

class ContactBase(BaseModel):
    phone_number: str

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    status: str

    class Config:
        from_attributes = True

class CampaignBase(BaseModel):
    name: str
    agent_id: int

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    status: str
    contacts: List[Contact] = []

    class Config:
        from_attributes = True