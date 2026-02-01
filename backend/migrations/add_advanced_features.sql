-- Phase V: Advanced Features Migration

-- Add priority column
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium';

-- Add tags column
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS tags TEXT DEFAULT '';

-- Add due date
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS due_date TIMESTAMP;

-- Add reminder time
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS reminder_time TIMESTAMP;

-- Add recurring task support
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE;

ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS recurrence_type VARCHAR(20);

ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS recurrence_interval INTEGER DEFAULT 1;

ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS parent_task_id INTEGER;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_tags ON tasks USING gin(to_tsvector('english', tags));

-- Create audit log table
CREATE TABLE IF NOT EXISTS task_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    task_id INTEGER,
    user_id VARCHAR(255) NOT NULL,
    event_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_events_task ON task_events(task_id);
CREATE INDEX IF NOT EXISTS idx_events_user ON task_events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_type ON task_events(event_type);
