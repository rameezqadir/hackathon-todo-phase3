from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RecurrenceType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Task(SQLModel, table=True):
priority: str = Field(default="medium")
    tags: str = Field(default="")
    due_date: Optional[datetime] = None
    reminder_time: Optional[datetime] = None
    is_recurring: bool = Field(default=False)
    recurrence_type: Optional[str] = None
    recurrence_interval: int = Field(default=1)
    parent_task_id: Optional[int] = None

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    title: str = Field(max_length=200, nullable=False)
    description: str = Field(default="")
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TaskCreate(SQLModel):
    title: str = Field(max_length=200, min_length=1)
    description: str = Field(default="", max_length=1000)


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskResponse(SQLModel):
    id: int
    user_id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class Conversation(SQLModel, table=True):
    """Conversation model for chat sessions."""

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Message(SQLModel, table=True):
    """Message model for chat history."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(index=True, nullable=False)
    role: str = Field(nullable=False)  # "user" or "assistant"
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)


class ChatRequest(SQLModel):
    """Schema for chat request."""
    message: str = Field(min_length=1)
    conversation_id: Optional[int] = None


class ChatResponse(SQLModel):
    """Schema for chat response."""
    conversation_id: int
    response: str
    tool_calls: List[str] = []
