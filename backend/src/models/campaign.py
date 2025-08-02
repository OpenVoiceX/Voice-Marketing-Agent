# backend/src/models/campaign.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    status = Column(String, default="draft", nullable=False) # e.g., "draft", "running", "paused", "completed"
    
    agent_id = Column(Integer, ForeignKey("agents.id"))
    agent = relationship("Agent")
    
    contacts = relationship("Contact", back_populates="campaign")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True, nullable=False)
    status = Column(String, default="pending", nullable=False) # e.g., "pending", "calling", "completed", "failed"
    
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    campaign = relationship("Campaign", back_populates="contacts")