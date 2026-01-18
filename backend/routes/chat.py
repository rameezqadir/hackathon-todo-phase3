"""
Chat API Routes - Handle AI chat conversations
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ai_agent import AIAgent

router = APIRouter(prefix="/api", tags=["chat"])

# Initialize AI agent globally
ai_agent = AIAgent()


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[str]
    message_id: int
    timestamp: datetime

class ConversationInfo(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    message_count: int

class MessageInfo(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_with_ai(
    user_id: str,
    request: ChatRequest
):
    """
    Main chat endpoint for AI-powered todo management.
    
    Args:
        user_id: The user's ID
        request: Chat request with message and optional conversation_id
        
    Returns:
        AI response with conversation information
    """
    try:
        result = await ai_agent.process_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result["tool_calls"],
            message_id=result.get("message_id", 0),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/{user_id}/chat/conversations", response_model=List[ConversationInfo])
async def get_conversations(user_id: str):
    """
    Get all conversations for a user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        List of conversation information
    """
    try:
        conversations = ai_agent.get_conversations(user_id)
        return conversations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get conversations: {str(e)}"
        )


@router.get("/{user_id}/chat/conversations/{conversation_id}/messages", response_model=List[MessageInfo])
async def get_conversation_messages(user_id: str, conversation_id: int):
    """
    Get all messages in a conversation.
    
    Args:
        user_id: The user's ID
        conversation_id: The conversation ID
        
    Returns:
        List of messages in the conversation
    """
    try:
        messages = ai_agent.get_conversation_messages(conversation_id, user_id)
        return messages
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get conversation messages: {str(e)}"
        )
