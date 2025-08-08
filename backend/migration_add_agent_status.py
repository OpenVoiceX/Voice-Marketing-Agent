# backend/migration_add_agent_status.py
from sqlalchemy import create_engine, text
from src.core.config import settings

def migrate_agent_status():
    """Add status fields to existing agents table"""
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Add the new columns
        try:
            conn.execute(text("ALTER TABLE agents ADD COLUMN last_call_status VARCHAR DEFAULT 'idle'"))
            conn.execute(text("ALTER TABLE agents ADD COLUMN last_call_time TIMESTAMP"))
            conn.commit()
            print("✅ Successfully added status columns to agents table")
        except Exception as e:
            print(f"⚠️ Migration may have already run or failed: {e}")

if __name__ == "__main__":
    migrate_agent_status()