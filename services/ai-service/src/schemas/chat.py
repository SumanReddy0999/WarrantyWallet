import uuid
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Pydantic model for the chat request body."""
    warranty_id: uuid.UUID
    question: str

class ChatResponse(BaseModel):
    """Pydantic model for the chat response body."""
    answer: str