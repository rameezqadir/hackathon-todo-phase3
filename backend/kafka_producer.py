"""
Kafka Producer Service
Publishes events to Kafka topics
"""

from kafka import KafkaProducer
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class TodoKafkaProducer:
    """Kafka producer for todo events"""
    
    def __init__(self, bootstrap_servers='localhost:9092'):
        """Initialize Kafka producer"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                acks='all',
                retries=3
            )
            logger.info("✅ Kafka producer initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Kafka: {e}")
            self.producer = None
    
    def publish_task_event(self, event_type: str, task_id: int, user_id: str, task_data: dict):
        """Publish task event to Kafka"""
        if not self.producer:
            logger.warning("⚠️  Kafka producer not available")
            return
        
        event = {
            'event_type': event_type,
            'task_id': task_id,
            'user_id': user_id,
            'task_data': task_data,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            future = self.producer.send('task-events', value=event)
            future.get(timeout=10)
            logger.info(f"📤 Published {event_type} event for task {task_id}")
        except Exception as e:
            logger.error(f"❌ Failed to publish event: {e}")
    
    def publish_reminder(self, task_id: int, user_id: str, title: str, due_at: str):
        """Publish reminder event"""
        if not self.producer:
            return
        
        event = {
            'task_id': task_id,
            'user_id': user_id,
            'title': title,
            'due_at': due_at,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            future = self.producer.send('reminders', value=event)
            future.get(timeout=10)
            logger.info(f"📤 Published reminder for task {task_id}")
        except Exception as e:
            logger.error(f"❌ Failed to publish reminder: {e}")
    
    def close(self):
        """Close producer"""
        if self.producer:
            self.producer.close()
            logger.info("⏹️  Kafka producer closed")


# Global producer instance
kafka_producer = TodoKafkaProducer()
