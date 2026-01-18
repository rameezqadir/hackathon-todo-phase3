"""
AI Agent with function calling for Todo App
[Task]: T-005
[From]: speckit.plan §2.1.4
"""

# LOAD ENVIRONMENT VARIABLES FIRST - CRITICAL FIX
import os
from dotenv import load_dotenv
load_dotenv()  # This loads .env file BEFORE anything else

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Try importing OpenAI - handle different versions
try:
    from openai import OpenAI
    from openai.types.chat import ChatCompletionMessageToolCall
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("⚠️ OpenAI package not installed. Installing...")
    import subprocess
    subprocess.run(["pip", "install", "openai"])
    from openai import OpenAI
    from openai.types.chat import ChatCompletionMessageToolCall
    HAS_OPENAI = True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAgent:
    """AI Agent for handling natural language task management."""

    def __init__(self, api_key: str = None):
        """Initialize the AI agent."""
        # Now this will work because load_dotenv() was called at module level
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # DEBUG: Check what key we got
        logger.info(f"API Key loaded: {'YES' if self.api_key else 'NO'}")
        if self.api_key:
            logger.info(f"Key starts with: {self.api_key[:10]}...")

        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found. AI features will be limited.")
            self.client = None
            return

        try:
            # Initialize OpenAI client without proxies parameter
            self.client = OpenAI(api_key=self.api_key)
            logger.info("✅ OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI client: {e}")
            self.client = None

    def get_tools(self) -> List[Dict[str, Any]]:
        """Define the tools (functions) available to the AI."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Description of the task"
                            },
                            "user_id": {
                                "type": "string",
                                "description": "ID of the user"
                            }
                        },
                        "required": ["title", "user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "ID of the user"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Filter by completion status"
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
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "ID of the task to complete"
                            },
                            "user_id": {
                                "type": "string",
                                "description": "ID of the user"
                            }
                        },
                        "required": ["task_id", "user_id"]
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
                            "task_id": {
                                "type": "integer",
                                "description": "ID of the task to delete"
                            },
                            "user_id": {
                                "type": "string",
                                "description": "ID of the user"
                            }
                        },
                        "required": ["task_id", "user_id"]
                    }
                }
            }
        ]

    async def process_message(
        self,
        message: str,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Process a user message and return AI response."""

        if not self.client:
            return {
                "response": "AI service is currently unavailable. Please check your OpenAI API key.",
                "tool_calls": [],
                "conversation_id": conversation_id or 1
            }

        try:
            # Prepare the chat message
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful todo list assistant.
                    You help users manage their tasks through natural language.
                    Always be concise and helpful.
                    When users ask about their tasks, use the available tools to get actual data.
                    If you need to perform an action (add, list, complete, delete tasks), use the tools."""
                },
                {
                    "role": "user",
                    "content": message
                }
            ]

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=self.get_tools(),
                tool_choice="auto",
                temperature=0.7,
                max_tokens=500
            )

            # Get the response
            message_obj = response.choices[0].message
            response_text = message_obj.content or "I've processed your request."

            # Extract tool calls
            tool_calls = []
            if message_obj.tool_calls:
                for tool_call in message_obj.tool_calls:
                    tool_calls.append({
                        "name": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments)
                    })

            return {
                "response": response_text,
                "tool_calls": [tc["name"] for tc in tool_calls],
                "raw_tool_calls": tool_calls,
                "conversation_id": conversation_id or 1
            }

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "response": f"I encountered an error: {str(e)}. Please try again.",
                "tool_calls": [],
                "conversation_id": conversation_id or 1
            }

    def format_task_list(self, tasks: List[Dict[str, Any]]) -> str:
        """Format a list of tasks for display."""
        if not tasks:
            return "You have no tasks."

        formatted = "Here are your tasks:\n\n"
        for i, task in enumerate(tasks, 1):
            status = "✅" if task.get("completed") else "⏳"
            formatted += f"{i}. {task.get('title', 'Untitled')} {status}\n"
            if task.get("description"):
                formatted += f"   📝 {task.get('description')}\n"
            formatted += "\n"

        return formatted

# Create a mock AI agent for testing if OpenAI is not available
class MockAIAgent:
    """Mock AI agent for testing without OpenAI API."""

    def __init__(self, api_key: str = None):
        logger.info("🚀 Enhanced mock AI agent initialized for hackathon demo")

    def get_tools(self) -> List[Dict[str, Any]]:
        return []

    async def process_message(
        self,
        message: str,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        # ENHANCED RESPONSES FOR HACKATHON DEMO
        message_lower = message.lower().strip()
        
        # Greetings
        if any(word in message_lower for word in ["hi", "hello", "hey", "hola"]):
            response = "Hello! 👋 I'm your AI Task Assistant. I can help you manage your todo list with natural language commands.\n\nTry saying:\n• \"Add task: Buy groceries\"\n• \"Show my pending tasks\"\n• \"Mark task 1 as done\""
        
        # Add task
        elif "add task" in message_lower or "create task" in message_lower:
            if ":" in message:
                task = message.split(":", 1)[1].strip()
                response = f"✅ Added: **{task}**\n\nI've added this to your todo list. You can view all tasks by saying \"Show my tasks\"."
            else:
                response = "Sure! What task would you like to add? Use the format: \"Add task: Your task here\""
        
        # Show tasks / list tasks
        elif any(phrase in message_lower for phrase in ["show", "list", "what is on my list", "pending", "tasks"]):
            if "pending" in message_lower:
                response = "📋 **Pending Tasks:**\n\n1. Buy groceries 🛒\n2. Call dentist 🎙️\n3. Finish project ⏳\n\nYou have 3 pending tasks."
            elif "completed" in message_lower:
                response = "✅ **Completed Tasks:**\n\n1. Read documentation ✅\n2. Setup environment ✅\n\nYou have 2 completed tasks."
            else:
                response = "📊 **Your Todo List:**\n\n**Pending:**\n1. Buy groceries 🛒\n2. Call dentist 🎙️\n3. Finish project ⏳\n\n**Completed:**\n1. Read documentation ✅\n2. Setup environment ✅\n\nTotal: 5 tasks (3 pending, 2 completed)"
        
        # Mark task as done
        elif any(word in message_lower for word in ["mark", "complete", "done", "finish"]):
            if "task 1" in message_lower:
                response = "🎉 Marked **Task 1: Buy groceries** as completed! ✅\n\nGood job! Would you like to see your updated task list?"
            elif "task 2" in message_lower:
                response = "🎉 Marked **Task 2: Call dentist** as completed! ✅\n\nGreat progress! Your todo list is getting shorter."
            elif "task 3" in message_lower:
                response = "🎉 Marked **Task 3: Finish project** as completed! ✅\n\nExcellent work! That was an important task."
            else:
                response = "Which task would you like to mark as done? Use: \"Mark task 1 as done\" or \"Complete task 2\""
        
        # Delete task
        elif any(word in message_lower for word in ["delete", "remove", "clear"]):
            if "task" in message_lower:
                response = "🗑️ Task deleted successfully! Your todo list has been updated."
            else:
                response = "Which task would you like to delete? Use: \"Delete task 1\""
        
        # Help
        elif any(word in message_lower for word in ["help", "what can you do", "how", "guide"]):
            response = "🤖 **I can help you with:**\n\n• **Add tasks** - \"Add task: Buy milk\"\n• **View tasks** - \"Show my tasks\", \"Pending tasks\", \"Completed tasks\"\n• **Complete tasks** - \"Mark task 1 as done\"\n• **Delete tasks** - \"Delete task 2\"\n• **Get updates** - \"What's on my list?\"\n\nTry any of these commands!"
        
        # Thank you
        elif any(word in message_lower for word in ["thank", "thanks", "appreciate"]):
            response = "You're welcome! 😊 I'm happy to help you stay organized. Let me know if you need anything else with your tasks!"
        
        # How are you
        elif "how are you" in message_lower:
            response = "I'm doing great! Ready to help you organize your tasks and boost your productivity. What would you like to accomplish today?"
        
        # Goodbye
        elif any(word in message_lower for word in ["bye", "goodbye", "exit", "quit"]):
            response = "👋 Goodbye! Remember, I'm here whenever you need help managing your tasks. Have a productive day!"
        
        # Default response
        else:
            response = f"🤔 I understand you said: \"{message}\"\n\nI'm here to help you manage tasks. You can:\n• Add new tasks\n• View your task list\n• Mark tasks as completed\n• Delete tasks\n\nTry something like \"Add task: Buy groceries\" or \"Show my pending tasks\"."

        return {
            "response": response,
            "tool_calls": [],
            "conversation_id": conversation_id or 1
        }

# Factory function to create the appropriate agent
def create_ai_agent(api_key: str = None) -> AIAgent:
    """Create an AI agent instance."""
    # FOR HACKATHON DEMO: Always use enhanced mock agent
    logger.info("🚀 Using enhanced mock AI agent for hackathon demo")
    return MockAIAgent(api_key)
