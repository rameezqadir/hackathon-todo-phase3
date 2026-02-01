"""
Reminder Consumer
Processes reminder events
"""

from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_reminder(event):
    """Process reminder event"""
    task_id = event.get('task_id')
    title = event.get('title')
    logger.info(f"🔔 REMINDER: {title} (Task {task_id})")
    # In production: send email/push notification


def main():
    """Main consumer loop"""
    consumer = KafkaConsumer(
        'reminders',
        bootstrap_servers='localhost:9092',
        group_id='reminder-service',
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest'
    )
    
    logger.info("✅ Reminder consumer started")
    
    for message in consumer:
        try:
            process_reminder(message.value)
        except Exception as e:
            logger.error(f"❌ Error processing reminder: {e}")


if __name__ == "__main__":
    main()
