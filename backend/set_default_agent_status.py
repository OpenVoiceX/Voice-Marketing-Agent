# backend/set_default_agent_status.py
"""
Quick script to set default 'idle' status for existing agents.
Run this once after adding the last_call_status field.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.database import SessionLocal
from src.models.agent import Agent

def set_default_status():
    """Set default 'idle' status for existing agents."""
    
    print("🔄 Setting default status for existing agents...")
    
    db = SessionLocal()
    try:
        # Get all agents
        agents = db.query(Agent).all()
        
        updated_count = 0
        for agent in agents:
            # Set to idle if no status or empty status
            if not hasattr(agent, 'last_call_status') or not agent.last_call_status:
                agent.last_call_status = 'idle'
                updated_count += 1
        
        db.commit()
        print(f"✅ Updated {updated_count} agents to 'idle' status")
        print(f"📊 Total agents in database: {len(agents)}")
        
        # Show current status of all agents
        print("\n📋 Current agent statuses:")
        for agent in agents:
            print(f"  Agent {agent.id} ({agent.name}): {agent.last_call_status}")
        
    except Exception as e:
        print(f"❌ Error updating agents: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    set_default_status()