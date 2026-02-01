"""
Recurring Task Consumer
Listens for completed tasks and creates next occurrence if recurring
"""

from kafka import KafkaConsumer
import json
from sqlmodel import Session, select
from database import engine
from models import Task
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_next_date(current_date, recurrence_type, interval):
    """Calculate next occurrence date"""
    if recurrence_type == 'daily':
        return current_date + timedelta(days=interval)
    elif recurrence_type == 'weekly':
        return current_date + timedelta(weeks=interval)
    elif recurrence_type == 'monthly':
        return current_date + timedelta(days=30 * interval)
    elif recurrence_type == 'yearly':
        return current_date + timedelta(days=365 * interval)
    return current_date + timedelta(days=1)


def process_completed_task(event):
    """Process completed task and create next occurrence if recurring"""
    task_data = event.get('task_data', {})
    
    if not task_data.get('is_recurring'):
        return
    
    task_id = event.get('task_id')
    user_id = event.get('user_id')
    
    logger.info(f"♻️  Creating next occurrence for task {task_id}")
    
    # Calculate next due date
    next_due = calculate_next_date(
        datetime.now(),
        task_data.get('recurrence_type', 'daily'),
        task_data.get('recurrence_interval', 1)
    )
    
    # Create new task
    with Session(engine) as session:
        new_task = Task(
            user_id=user_id,
            title=task_data.get('title'),
            description=task_data.get('description', ''),
            priority=task_data.get('priority', 'medium'),
            tags=task_data.get('tags', ''),
            due_date=next_due,
            is_recurring=True,
            recurrence_type=task_data.get('recurrence_type'),
            recurrence_interval=task_data.get('recurrence_interval', 1),
            parent_task_id=task_id
        )
        session.add(new_task)
        session.commit()
        logger.info(f"✅ Created next occurrence: Task {new_task.id}")


def main():
    """Main consumer loop"""
    consumer = KafkaConsumer(
        'task-events',
        bootstrap_servers='localhost:9092',
        group_id='recurring-task-service',
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest'
    )
    
    logger.info("✅ Recurring task consumer started")
    
    for message in consumer:
        event = message.value
        if event.get('event_type') == 'completed':
            try:
                process_completed_task(event)
            except Exception as e:
                logger.error(f"❌ Error processing event: {e}")


if __name__ == "__main__":
    main()
