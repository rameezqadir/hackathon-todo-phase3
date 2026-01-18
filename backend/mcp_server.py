"""
MCP Server - Exposes task operations as tools for AI agent
"""

from typing import Dict, Any, Optional
from sqlmodel import Session, select
from database import engine
from models import Task
from datetime import datetime


class MCPServer:
    """MCP Server that provides task operation tools."""
    
    def __init__(self):
        """Initialize MCP server."""
        self.tools = {
            "add_task": self.add_task,
            "list_tasks": self.list_tasks,
            "complete_task": self.complete_task,
            "delete_task": self.delete_task,
            "update_task": self.update_task,
        }
    
    def add_task(self, user_id: str, title: str, description: str = "") -> Dict[str, Any]:
        """
        Add a new task.
        
        Args:
            user_id: User identifier
            title: Task title
            description: Task description (optional)
            
        Returns:
            Dict with task_id, status, and title
        """
        with Session(engine) as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
    
    def list_tasks(self, user_id: str, status: str = "all") -> Dict[str, Any]:
        """
        List user's tasks.
        
        Args:
            user_id: User identifier
            status: Filter by status (all/pending/completed)
            
        Returns:
            Dict with tasks array
        """
        with Session(engine) as session:
            statement = select(Task).where(Task.user_id == user_id)
            
            if status == "pending":
                statement = statement.where(Task.completed == False)
            elif status == "completed":
                statement = statement.where(Task.completed == True)
            
            tasks = session.exec(statement).all()
            
            return {
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat()
                    }
                    for task in tasks
                ]
            }
    
    def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        Mark task as complete.
        
        Args:
            user_id: User identifier
            task_id: Task identifier
            
        Returns:
            Dict with task_id, status, and title
        """
        with Session(engine) as session:
            task = session.get(Task, task_id)
            
            if not task or task.user_id != user_id:
                return {
                    "task_id": task_id,
                    "status": "error",
                    "message": "Task not found"
                }
            
            task.completed = not task.completed
            task.updated_at = datetime.now()
            session.add(task)
            session.commit()
            
            return {
                "task_id": task.id,
                "status": "completed" if task.completed else "reopened",
                "title": task.title
            }
    
    def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """
        Delete a task.
        
        Args:
            user_id: User identifier
            task_id: Task identifier
            
        Returns:
            Dict with task_id, status, and title
        """
        with Session(engine) as session:
            task = session.get(Task, task_id)
            
            if not task or task.user_id != user_id:
                return {
                    "task_id": task_id,
                    "status": "error",
                    "message": "Task not found"
                }
            
            title = task.title
            session.delete(task)
            session.commit()
            
            return {
                "task_id": task_id,
                "status": "deleted",
                "title": title
            }
    
    def update_task(
        self, 
        user_id: str, 
        task_id: int, 
        title: Optional[str] = None, 
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a task.
        
        Args:
            user_id: User identifier
            task_id: Task identifier
            title: New title (optional)
            description: New description (optional)
            
        Returns:
            Dict with task_id, status, and title
        """
        with Session(engine) as session:
            task = session.get(Task, task_id)
            
            if not task or task.user_id != user_id:
                return {
                    "task_id": task_id,
                    "status": "error",
                    "message": "Task not found"
                }
            
            if title:
                task.title = title
            if description is not None:
                task.description = description
            
            task.updated_at = datetime.now()
            session.add(task)
            session.commit()
            
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
    
    def get_tool_definitions(self) -> list:
        """Get OpenAI function definitions for all tools."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List user's tasks",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"]
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete or incomplete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "task_id": {"type": "integer"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "task_id": {"type": "integer"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update task title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string"},
                            "task_id": {"type": "integer"},
                            "title": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]
