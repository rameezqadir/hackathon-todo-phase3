"""
Main FastAPI application for Todo App Phase III
[Task]: T-001
[From]: speckit.plan §2.1
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from typing import List
import os

from database import engine, get_session, create_db_and_tables
from models import Task, TaskCreate, TaskUpdate, TaskResponse
from models import Conversation, Message, ChatRequest, ChatResponse
from ai_agent import create_ai_agent

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create AI agent
ai_agent = create_ai_agent(OPENAI_API_KEY)

# Create FastAPI app
app = FastAPI(title="Todo App API - Phase III", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    create_db_and_tables()
    print("✅ Database initialized")
    
    # Check AI agent status
    if hasattr(ai_agent, 'client') and ai_agent.client:
        print("✅ AI Agent initialized successfully")
    else:
        print("⚠️  AI Agent running in mock mode (no OpenAI API key)")

# Health check
@app.get("/")
def read_root():
    return {"message": "Todo App API - Phase III", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}

# Tasks endpoints
@app.get("/api/{user_id}/tasks", response_model=List[TaskResponse])
def get_tasks(user_id: str, session: Session = Depends(get_session)):
    """Get all tasks for a user"""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

@app.get("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(user_id: str, task_id: int, session: Session = Depends(get_session)):
    """Get a specific task"""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/{user_id}/tasks", response_model=TaskResponse)
def create_task(user_id: str, task: TaskCreate, session: Session = Depends(get_session)):
    """Create a new task"""
    db_task = Task(**task.dict(), user_id=user_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.put("/api/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str, 
    task_id: int, 
    task_update: TaskUpdate, 
    session: Session = Depends(get_session)
):
    """Update a task"""
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Update only provided fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.delete("/api/{user_id}/tasks/{task_id}")
def delete_task(user_id: str, task_id: int, session: Session = Depends(get_session)):
    """Delete a task"""
    task = session.get(Task, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}

# Chat endpoint with AI integration
@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_with_ai(
    user_id: str, 
    chat_request: ChatRequest, 
    session: Session = Depends(get_session)
):
    """Chat with AI assistant"""
    
    # Process message with AI agent
    result = await ai_agent.process_message(
        message=chat_request.message,
        user_id=user_id,
        conversation_id=chat_request.conversation_id
    )
    
    # Handle tool calls if any
    if result.get("raw_tool_calls"):
        for tool_call in result["raw_tool_calls"]:
            try:
                await handle_tool_call(tool_call, user_id, session)
            except Exception as e:
                print(f"Error handling tool call: {e}")
    
    return ChatResponse(
        conversation_id=result["conversation_id"],
        response=result["response"],
        tool_calls=result["tool_calls"]
    )

async def handle_tool_call(tool_call: dict, user_id: str, session: Session):
    """Handle tool calls from AI agent."""
    tool_name = tool_call["name"]
    arguments = tool_call["arguments"]
    
    # Ensure user_id matches
    arguments["user_id"] = user_id
    
    if tool_name == "add_task":
        # Create task from AI request
        task_data = TaskCreate(
            title=arguments["title"],
            description=arguments.get("description", "")
        )
        db_task = Task(**task_data.dict(), user_id=user_id)
        session.add(db_task)
        session.commit()
        print(f"✅ AI added task: {arguments['title']}")
        
    elif tool_name == "list_tasks":
        # Tasks will be listed in the AI response
        print(f"✅ AI listed tasks for user: {user_id}")
        
    elif tool_name == "complete_task":
        # Mark task as completed
        task_id = arguments["task_id"]
        task = session.get(Task, task_id)
        if task and task.user_id == user_id:
            task.completed = True
            session.add(task)
            session.commit()
            print(f"✅ AI completed task: {task_id}")
        
    elif tool_name == "delete_task":
        # Delete task
        task_id = arguments["task_id"]
        task = session.get(Task, task_id)
        if task and task.user_id == user_id:
            session.delete(task)
            session.commit()
            print(f"✅ AI deleted task: {task_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from event_handler import event_bus

# Add to task creation endpoint
@app.post("/api/{user_id}/tasks")
def create_task_with_events(user_id: str, task: TaskCreate):
    # ... existing creation code ...
    
    # Publish event
    event_bus.publish('task.created', {
        'task_id': db_task.id,
        'user_id': user_id,
        'title': task.title
    })
    
    return db_task

# Add to task completion endpoint
@app.patch("/api/{user_id}/tasks/{task_id}/complete")
def complete_task_with_events(user_id: str, task_id: int):
    # ... existing completion code ...
    
    # Publish event
    event_bus.publish('task.completed', {
        'task_id': task_id,
        'user_id': user_id,
        'is_recurring': task.is_recurring
    })
    
    return task
