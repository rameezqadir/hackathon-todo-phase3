"""Phase V Migration"""
from sqlmodel import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def migrate():
    with engine.connect() as conn:
        # Read SQL file
        with open('add_advanced_fields.sql', 'r') as f:
            sql = f.read()
        
        # Execute each statement
        for statement in sql.split(';'):
            if statement.strip():
                conn.execute(text(statement))
        
        conn.commit()
        print("✅ Phase V migration complete!")

if __name__ == "__main__":
    migrate()
