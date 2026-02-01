from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uvicorn
import json
from kafka import KafkaProducer, KafkaConsumer
from enum import Enum
import asyncio

app = FastAPI(
    title="Todo App API - Phase V",
    description="Advanced features with Kafka event streaming",
    version="5.0.0"
)

# ===== PHASE V ENHANCEMENTS =====
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RecurrenceType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class TaskCreatePhase5(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Priority = Field(default=Priority.MEDIUM)
    tags: List[str] = Field(default_factory=list)
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    is_recurring: bool = Field(default=False)
    recurrence_type: Optional[RecurrenceType] = None
    recurrence_interval: int = Field(default=1, ge=1)

# ===== KAFKA SETUP =====
KAFKA_BOOTSTRAP = "todo-kafka:9092"
KAFKA_TOPIC_TASKS = "todo-tasks"
KAFKA_TOPIC_EVENTS = "todo-events"

try:
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BOOTSTRAP],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
        acks='all',
        retries=3
    )
    KAFKA_ENABLED = True
    print(f"✅ Kafka Producer connected to {KAFKA_BOOTSTRAP}")
except Exception as e:
    print(f"⚠️ Kafka Producer disabled: {e}")
    producer = None
    KAFKA_ENABLED = False

# ===== IN-MEMORY STORAGE =====
tasks_db = {}
task_id_counter = 1

# ===== API ENDPOINTS =====
@app.get("/")
async def root():
    return {
        "message": "Todo App API - Phase V",
        "version": "5.0.0",
        "features": [
            "Advanced task attributes (priority, tags, due dates)",
            "Kafka event streaming",
            "Recurring tasks",
            "Reminders",
            "Backward compatible with Phase III"
        ],
        "kafka": "enabled" if KAFKA_ENABLED else "disabled",
        "endpoints": {
            "phase3_compatible": "POST /api/{user_id}/tasks",
            "phase5_advanced": "POST /api/{user_id}/tasks/advanced",
            "get_tasks": "GET /api/{user_id}/tasks",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "phase": "V",
        "timestamp": datetime.utcnow().isoformat(),
        "kafka": KAFKA_ENABLED,
        "tasks_count": len(tasks_db)
    }

# Backward compatible Phase III endpoint
@app.post("/api/{user_id}/tasks")
async def create_task_phase3(user_id: str, task: dict):
    """Phase III compatible endpoint"""
    global task_id_counter
    
    task_data = {
        "id": task_id_counter,
        "user_id": user_id,
        "title": task.get("title", "Untitled"),
        "description": task.get("description"),
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "phase": "III"
    }
    
    tasks_db[task_id_counter] = task_data
    task_id_counter += 1
    
    return task_data

# Phase V Advanced endpoint
@app.post("/api/{user_id}/tasks/advanced")
async def create_advanced_task(user_id: str, task: TaskCreatePhase5):
    """Phase V endpoint with advanced features and Kafka integration"""
    global task_id_counter
    
    # Create task with advanced features
    task_data = {
        "id": task_id_counter,
        "user_id": user_id,
        "title": task.title,
        "description": task.description,
        "priority": task.priority.value,
        "tags": task.tags,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "reminder_time": task.reminder_time.isoformat() if task.reminder_time else None,
        "is_recurring": task.is_recurring,
        "recurrence_type": task.recurrence_type.value if task.recurrence_type else None,
        "recurrence_interval": task.recurrence_interval,
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "phase": "V"
    }
    
    tasks_db[task_id_counter] = task_data
    
    # Send event to Kafka
    kafka_event_sent = False
    if KAFKA_ENABLED and producer:
        try:
            event = {
                "event_type": "TASK_CREATED_ADVANCED",
                "event_id": f"evt_{task_id_counter}_{datetime.utcnow().timestamp()}",
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "task_id": task_id_counter,
                "task_data": task_data,
                "features_used": ["priority", "tags", "due_date", "kafka"]
            }
            
            # Send to both topics for demonstration
            producer.send(KAFKA_TOPIC_TASKS, task_data)
            producer.send(KAFKA_TOPIC_EVENTS, event)
            producer.flush()
            
            kafka_event_sent = True
            print(f"📨 Phase V task sent to Kafka: {task.title}")
            
        except Exception as e:
            print(f"❌ Kafka error: {e}")
    
    task_id_counter += 1
    
    return {
        "message": "Advanced task created successfully (Phase V)",
        "task": task_data,
        "kafka": {
            "enabled": KAFKA_ENABLED,
            "event_sent": kafka_event_sent,
            "topics": [KAFKA_TOPIC_TASKS, KAFKA_TOPIC_EVENTS] if kafka_event_sent else None
        },
        "advanced_features": [
            "priority_system",
            "tagging",
            "due_dates",
            "reminders",
            "recurrence",
            "kafka_integration"
        ]
    }

@app.get("/api/{user_id}/tasks")
async def get_user_tasks(user_id: str, phase: Optional[str] = None):
    """Get tasks for a user, filter by phase if specified"""
    user_tasks = [task for task in tasks_db.values() if task["user_id"] == user_id]
    
    if phase:
        user_tasks = [task for task in user_tasks if task.get("phase") == phase]
    
    return {
        "user_id": user_id,
        "phase_filter": phase,
        "tasks": user_tasks,
        "count": len(user_tasks),
        "phases_available": list(set(t.get("phase") for t in user_tasks))
    }

@app.get("/api/stats")
async def get_stats():
    """Get statistics about tasks"""
    total_tasks = len(tasks_db)
    phase_v_tasks = sum(1 for t in tasks_db.values() if t.get("phase") == "V")
    phase_iii_tasks = total_tasks - phase_v_tasks
    
    # Priority distribution
    priorities = {}
    for task in tasks_db.values():
        if task.get("phase") == "V":
            priority = task.get("priority", "medium")
            priorities[priority] = priorities.get(priority, 0) + 1
    
    return {
        "total_tasks": total_tasks,
        "phase_v_tasks": phase_v_tasks,
        "phase_iii_tasks": phase_iii_tasks,
        "priority_distribution": priorities,
        "kafka_enabled": KAFKA_ENABLED
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TODo APP API - PHASE V")
    print("=" * 60)
    print("📊 Features:")
    print("  • Priority system (low, medium, high, critical)")
    print("  • Tagging support")
    print("  • Due dates and reminders")
    print("  • Recurring tasks")
    print("  • Kafka event streaming")
    print("  • Backward compatible with Phase III")
    print("")
    print("📡 Endpoints:")
    print("  • POST /api/{user_id}/tasks           (Phase III compatible)")
    print("  • POST /api/{user_id}/tasks/advanced  (Phase V advanced)")
    print("  • GET  /api/{user_id}/tasks           (List tasks)")
    print("  • GET  /api/stats                     (Statistics)")
    print("  • GET  /health                        (Health check)")
    print("")
    print(f"📊 Kafka: {'✅ CONNECTED' if KAFKA_ENABLED else '⚠️ DISABLED'}")
    if KAFKA_ENABLED:
        print(f"   Topics: {KAFKA_TOPIC_TASKS}, {KAFKA_TOPIC_EVENTS}")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
