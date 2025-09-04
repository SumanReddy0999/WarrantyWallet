from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BaseSchema(BaseModel):
    """Base schema with common fields and configurations"""
    class Config:
        from_attributes = True  # For SQLAlchemy model compatibility
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }
        extra = "ignore"  # Ignore extra fields during model validation
