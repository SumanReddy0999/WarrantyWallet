from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class NotificationBase(BaseModel):
    notification_type: str = Field(..., description="Type of notification")
    content: str = Field(..., description="Notification content")
    status: str = Field(default="unread", description="Notification status (e.g., 'unread', 'read')")
    warranty_id: UUID = Field(..., description="Related warranty ID")

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Notification status (e.g., 'read')")

class NotificationResponse(NotificationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
