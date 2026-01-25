"""
Simple Event System (without Kafka)
For local development and demonstration
"""

import json
from datetime import datetime
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class SimpleEventBus:
    """In-memory event bus for local development"""
    
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.handlers = {
            'task.created': [],
            'task.completed': [],
            'task.deleted': [],
            'reminder.due': []
        }
    
    def publish(self, event_type: str, data: Dict[str, Any]):
        """Publish an event"""
        event = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        self.events.append(event)
        logger.info(f"📤 Event published: {event_type}")
        
        # Call handlers
        for handler in self.handlers.get(event_type, []):
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Handler error: {e}")
    
    def subscribe(self, event_type: str, handler):
        """Subscribe to an event"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
        logger.info(f"✅ Subscribed to: {event_type}")
    
    def get_events(self, event_type: str = None) -> List[Dict]:
        """Get events (for monitoring/audit)"""
        if event_type:
            return [e for e in self.events if e['type'] == event_type]
        return self.events


# Global event bus
event_bus = SimpleEventBus()


# Example handlers
def handle_task_completed(data: Dict[str, Any]):
    """Handle task completion - create recurring task if needed"""
    if data.get('is_recurring'):
        logger.info(f"♻️  Task {data['task_id']} is recurring - creating next occurrence")
        # In production, this would create the next task


def handle_reminder_due(data: Dict[str, Any]):
    """Handle reminder"""
    logger.info(f"🔔 Reminder: {data.get('title')}")
    # In production, send email/push notification


# Register handlers
event_bus.subscribe('task.completed', handle_task_completed)
event_bus.subscribe('reminder.due', handle_reminder_due)
