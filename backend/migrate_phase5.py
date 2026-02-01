"""
Phase V Database Migration
Adds advanced features to tasks table
"""

from sqlmodel import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not set in .env")
    exit(1)

engine = create_engine(DATABASE_URL, echo=True)

def run_migration():
    print("🔄 Running Phase V migration...")
    
    with engine.connect() as conn:
        # Read SQL file
        with open('migrations/add_advanced_features.sql', 'r') as f:
            sql = f.read()
        
        # Execute each statement
        for statement in sql.split(';'):
            if statement.strip():
                try:
                    conn.execute(text(statement))
                except Exception as e:
                    print(f"⚠️  Statement failed (may already exist): {e}")
        
        conn.commit()
        print("✅ Phase V migration completed!")

if __name__ == "__main__":
    run_migration()
