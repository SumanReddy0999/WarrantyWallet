from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class ChatMessageBase(BaseModel):
    content: str = Field(..., description="The message content")
    sender_type: str = Field(..., description="Type of sender (e.g., 'user', 'ai')")

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: UUID
    session_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    warranty_id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []
    
    class Config:
        from_attributes = True
