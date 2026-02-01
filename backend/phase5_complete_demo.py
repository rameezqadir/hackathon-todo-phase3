from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uvicorn
import json
from kafka import KafkaProducer, KafkaConsumer
from enum import Enum
import threading
import time
import asyncio

app = FastAPI(
    title="🎯 TODO APP - PHASE V COMPLETE DEMO",
    description="Demonstrating all Phase V features with Kafka integration",
    version="5.0.0"
)

# ===== CONFIGURATION =====
KAFKA_BOOTSTRAP = 'localhost:19092'
TOPICS = {
    'tasks': 'phase5-tasks',
    'events': 'task-events', 
    'reminders': 'reminders'
}

print("\n" + "="*70)
print("🚀 PHASE V - COMPLETE DEMONSTRATION")
print("="*70)
print(f"📊 Kafka: {KAFKA_BOOTSTRAP}")
print(f"📨 Topics: {', '.join(TOPICS.values())}")
print("="*70)

# ===== KAFKA SETUP =====
class KafkaManager:
    def __init__(self):
        self.producer = None
        self.consumers = {}
        self.connected = False
        self.setup_kafka()
    
    def setup_kafka(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=[KAFKA_BOOTSTRAP],
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                api_version=(2, 0, 2),
                request_timeout_ms=5000
            )
            
            # Test connection
            test_msg = {'phase': 'V', 'test': True, 'timestamp': time.time()}
            future = self.producer.send(TOPICS['events'], test_msg)
            future.get(timeout=5)
            
            self.connected = True
            print("✅ Kafka Producer: CONNECTED")
            
            # Start background consumer for demo
            self.start_event_consumer()
            
        except Exception as e:
            print(f"⚠️ Kafka Producer: DISCONNECTED - {str(e)[:80]}")
            self.connected = False
    
    def start_event_consumer(self):
        """Start a background consumer to show real-time events"""
        def consume_events():
            consumer = KafkaConsumer(
                TOPICS['events'],
                bootstrap_servers=[KAFKA_BOOTSTRAP],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='phase5-demo-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            
            print(f"👂 Listening for events on '{TOPICS['events']}' topic...")
            event_count = 0
            
            for message in consumer:
                event_count += 1
                event = message.value
                print(f"📨 Event #{event_count}: {event.get('event_type', 'unknown')}")
                if event_count >= 10:  # Limit for demo
                    break
        
        thread = threading.Thread(target=consume_events, daemon=True)
        thread.start()
    
    def send_event(self, event_type: str, data: dict):
        if not self.connected or not self.producer:
            return {"status": "kafka_disconnected", "mode": "simulated"}
        
        try:
            event = {
                "event_type": event_type,
                "event_id": f"{event_type}_{int(time.time())}",
                "timestamp": datetime.utcnow().isoformat(),
                "data": data,
                "phase": "V"
            }
            
            future = self.producer.send(TOPICS['events'], event)
            result = future.get(timeout=5)
            
            return {
                "status": "sent",
                "topic": TOPICS['events'],
                "partition": result.partition,
                "offset": result.offset,
                "event_id": event["event_id"]
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}

kafka_manager = KafkaManager()

# ===== MODELS =====
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Recurrence(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, 
                       example="Complete Phase V Implementation")
    description: Optional[str] = Field(None, 
                                      example="Implement all advanced features with Kafka")
    priority: Priority = Field(default=Priority.MEDIUM, example="high")
    tags: List[str] = Field(default_factory=list, 
                           example=["phase5", "kafka", "demo", "hackathon"])
    due_date: Optional[datetime] = Field(None, example="2026-01-28T23:59:59")
    reminder: bool = Field(default=False, example=True)
    is_recurring: bool = Field(default=False, example=False)
    recurrence: Optional[Recurrence] = Field(None, example="weekly")

# ===== DATA STORE =====
demo_tasks = []
task_counter = 1

# ===== API ENDPOINTS =====
@app.get("/")
async def root():
    return {
        "application": "Todo App - Phase V Complete Demo",
        "phase": "V (Advanced Features with Kafka)",
        "status": "operational",
        "kafka": "connected" if kafka_manager.connected else "simulated",
        "features": [
            "Advanced task attributes (priority, tags, due dates)",
            "Kafka event streaming",
            "Real-time event consumption",
            "Reminder system",
            "Recurring tasks",
            "Background processing"
        ],
        "endpoints": {
            "create_task": "POST /api/tasks/advanced",
            "list_tasks": "GET /api/tasks",
            "health": "GET /health",
            "kafka_status": "GET /kafka/status",
            "demo_stats": "GET /demo/stats"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "phase": "V",
        "kafka": kafka_manager.connected,
        "tasks_count": len(demo_tasks),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/kafka/status")
async def kafka_status():
    return {
        "connected": kafka_manager.connected,
        "bootstrap_server": KAFKA_BOOTSTRAP,
        "topics": TOPICS,
        "test_event": kafka_manager.send_event("STATUS_CHECK", {"check": "api"})
    }

@app.post("/api/tasks/advanced", 
          summary="Create Phase V task with all advanced features",
          response_description="Returns created task with Kafka event info")
async def create_advanced_task(task: TaskCreate, background_tasks: BackgroundTasks):
    global task_counter
    
    # Create task with all Phase V features
    task_data = {
        "id": task_counter,
        "title": task.title,
        "description": task.description,
        "priority": task.priority.value,
        "tags": task.tags,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "reminder_enabled": task.reminder,
        "is_recurring": task.is_recurring,
        "recurrence": task.recurrence.value if task.recurrence else None,
        "created_at": datetime.utcnow().isoformat(),
        "phase": "V",
        "features_used": [
            "priority_system",
            "tagging",
            "due_dates",
            "reminders",
            "recurrence_support"
        ]
    }
    
    demo_tasks.append(task_data)
    
    # Send to Kafka
    kafka_result = kafka_manager.send_event("TASK_CREATED_V5", task_data)
    
    # If reminder is enabled, schedule a reminder event
    if task.reminder and task.due_date:
        reminder_data = {
            "task_id": task_counter,
            "title": task.title,
            "due_date": task.due_date.isoformat(),
            "reminder_time": task.due_date.isoformat(),
            "user_notified": False
        }
        kafka_manager.send_event("REMINDER_SCHEDULED", reminder_data)
    
    task_counter += 1
    
    return {
        "message": "🎉 Phase V task created successfully!",
        "task": task_data,
        "kafka_event": kafka_result,
        "phase": "V",
        "demo_note": "All Phase V features demonstrated" if len(task_data["features_used"]) >= 3 else "Basic Phase V task"
    }

@app.get("/api/tasks")
async def list_tasks(priority: Optional[Priority] = None, tag: Optional[str] = None):
    filtered_tasks = demo_tasks
    
    if priority:
        filtered_tasks = [t for t in filtered_tasks if t.get("priority") == priority.value]
    
    if tag:
        filtered_tasks = [t for t in filtered_tasks if tag in t.get("tags", [])]
    
    # Send analytics event
    kafka_manager.send_event("TASKS_LISTED", {
        "filter_priority": priority.value if priority else None,
        "filter_tag": tag,
        "count": len(filtered_tasks)
    })
    
    return {
        "tasks": filtered_tasks,
        "count": len(filtered_tasks),
        "filters": {
            "priority": priority.value if priority else "none",
            "tag": tag or "none"
        },
        "total_tasks": len(demo_tasks)
    }

@app.get("/demo/stats")
async def demo_stats():
    """Demo statistics endpoint"""
    if not demo_tasks:
        return {"message": "No tasks yet. Create some with POST /api/tasks/advanced"}
    
    # Priority distribution
    priorities = {}
    for task in demo_tasks:
        priority = task.get("priority", "unknown")
        priorities[priority] = priorities.get(priority, 0) + 1
    
    # Tag frequency
    tag_freq = {}
    for task in demo_tasks:
        for tag in task.get("tags", []):
            tag_freq[tag] = tag_freq.get(tag, 0) + 1
    
    # Features usage
    features_used = {}
    for task in demo_tasks:
        for feature in task.get("features_used", []):
            features_used[feature] = features_used.get(feature, 0) + 1
    
    return {
        "total_tasks": len(demo_tasks),
        "phase_v_tasks": len([t for t in demo_tasks if t.get("phase") == "V"]),
        "priority_distribution": priorities,
        "top_tags": dict(sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)[:5]),
        "features_usage": features_used,
        "kafka_events": kafka_manager.connected,
        "demo_ready": len(demo_tasks) > 0
    }

@app.get("/demo/reset")
async def demo_reset():
    """Reset demo data (for testing)"""
    global demo_tasks, task_counter
    demo_tasks = []
    task_counter = 1
    kafka_manager.send_event("DEMO_RESET", {"reset_at": datetime.utcnow().isoformat()})
    return {"message": "Demo data reset", "tasks_cleared": True}

# ===== STARTUP =====
if __name__ == "__main__":
    print("\n" + "="*70)
    print("📡 API ENDPOINTS READY:")
    print("   POST /api/tasks/advanced  - Create Phase V task (with Kafka)")
    print("   GET  /api/tasks           - List tasks (filter by priority/tag)")
    print("   GET  /health              - System health")
    print("   GET  /kafka/status        - Kafka connection status")
    print("   GET  /demo/stats          - Demo statistics")
    print("   GET  /demo/reset          - Reset demo data")
    print("\n🔧 EXAMPLE REQUEST:")
    print('''   curl -X POST http://localhost:8000/api/tasks/advanced \\
     -H "Content-Type: application/json" \\
     -d '{
       "title": "Phase V Hackathon Demo",
       "priority": "critical",
       "tags": ["phase5", "kafka", "demo"],
       "due_date": "2026-01-28T23:59:59",
       "reminder": true
     }' ''')
    print("\n🌐 Server starting at: http://localhost:8000")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
