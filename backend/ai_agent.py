"""
AI Agent for task processing
"""

from typing import Dict, Any, Optional
import json
import os

class AIAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY', '')
        self.system_prompt = """You are a helpful task assistant. 
        Help users manage their tasks efficiently."""
        
        # Check if we have API key for enhanced features
        self.has_openai = bool(self.api_key)
        if self.has_openai:
            print("✅ AI Agent initialized with OpenAI API")
        else:
            print("⚠️ AI Agent running in local mode (no OpenAI API)")
        
    def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process task with AI suggestions"""
        title = task_data.get('title', 'Untitled Task')
        priority = task_data.get('priority', 'medium')
        tags = task_data.get('tags', '')
        due_date = task_data.get('due_date')
        
        suggestions = {
            "title": title,
            "ai_suggestions": {
                "breakdown": f"Consider breaking '{title}' into smaller subtasks",
                "priority_review": f"Current priority '{priority}' seems appropriate",
                "tag_suggestions": "Consider adding more specific tags" if len(tags) < 10 else "Tags look good",
                "due_date_reminder": f"Due on {due_date}" if due_date else "No due date set"
            },
            "time_estimation": "30-60 minutes",
            "similar_tasks": [],
            "has_openai": self.has_openai
        }
        
        # If we have OpenAI API, add enhanced suggestions
        if self.has_openai:
            suggestions["ai_suggestions"]["enhanced"] = "Using OpenAI for advanced analysis"
        
        return suggestions
    
    def analyze_priority(self, task_data: Dict[str, Any]) -> str:
        """Analyze and suggest priority"""
        title = task_data.get('title', '').lower()
        if any(word in title for word in ['urgent', 'asap', 'critical', 'important', 'high']):
            return 'high'
        elif any(word in title for word in ['low', 'someday', 'maybe', 'optional']):
            return 'low'
        return 'medium'

def create_ai_agent(api_key: Optional[str] = None) -> AIAgent:
    """Factory function to create AI agent"""
    return AIAgent(api_key)

# Global instance for easy access (without API key by default)
ai_agent_instance = create_ai_agent()

if __name__ == "__main__":
    # Test the agent
    test_task = {
        "title": "Complete hackathon project",
        "priority": "high",
        "tags": "hackathon,urgent",
        "due_date": "2026-01-25T23:59:59"
    }
    result = ai_agent_instance.process_task(test_task)
    print(json.dumps(result, indent=2))
