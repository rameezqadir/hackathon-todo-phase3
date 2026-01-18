#!/usr/bin/env python3
"""Simple database test - synchronous version"""

from database import engine
from sqlalchemy import text

def test():
    print("Testing database connection...")
    try:
        # SYNC version - no "async"
        with engine.connect() as conn:
            # Test connection
            result = conn.execute(text("SELECT 1"))
            print(f"✅ Database connection successful: {result.fetchone()}")
            
            # Check if tables exist
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Existing tables: {tables}")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
