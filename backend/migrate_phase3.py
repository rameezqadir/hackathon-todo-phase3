#!/usr/bin/env python3
"""Database migration script for Phase III - SQLModel synchronous version"""

import sys
from pathlib import Path
from datetime import datetime

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from database import engine, create_db_and_tables
from models import Task, Conversation, Message
from sqlmodel import Session

def migrate_database():
    """Create all database tables using SQLModel"""
    print("🚀 Starting database migration (SQLModel Sync)...")
    
    try:
        # Initialize database (creates all tables)
        create_db_and_tables()
        print("✅ Tables created successfully!")
        
        # Verify tables exist
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name IN ('tasks', 'conversations', 'messages')
            """))
            
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Tables verified: {', '.join(tables)}")
            
            if len(tables) == 3:
                print("🎉 Database migration completed successfully!")
            else:
                print(f"⚠️  Warning: Expected 3 tables, found {len(tables)}")
                
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def test_connection():
    """Test database connection"""
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            db_version = result.fetchone()[0]
            print(f"🔗 Database connected: {db_version.split()[0]}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_sample_data():
    """Create sample data for testing"""
    try:
        with Session(engine) as session:
            # Create sample tasks
            tasks = [
                Task(
                    user_id="demo-user",
                    title="Buy groceries",
                    description="Milk, eggs, bread",
                    completed=False,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ),
                Task(
                    user_id="demo-user",
                    title="Call dentist",
                    description="Schedule appointment",
                    completed=False,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ),
                Task(
                    user_id="demo-user",
                    title="Finish project",
                    description="Complete phase III",
                    completed=True,
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ),
            ]
            
            for task in tasks:
                session.add(task)
            
            session.commit()
            print(f"📝 Created {len(tasks)} sample tasks")
            
    except Exception as e:
        print(f"⚠️  Could not create sample data: {e}")

def main():
    """Main migration function"""
    print("="*60)
    print("Phase III Database Migration (SQLModel Sync)")
    print("="*60)
    
    # Check environment
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found")
    
    # Test database connection
    if not test_connection():
        print("❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Run migration
    migrate_database()
    
    # Create sample data
    print("\n📝 Creating sample data...")
    create_sample_data()
    
    print("\n" + "="*60)
    print("✅ Migration complete! You can now start the backend server.")
    print("="*60)

if __name__ == "__main__":
    main()
