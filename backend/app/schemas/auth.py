from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from typing import Optional

class SignupRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    address: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    email: EmailStr = Field(..., max_length=255)
    service: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    auth_provider: str = Field(..., description="Authentication provider (e.g., 'email', 'google', 'facebook')")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: 'UserResponse'

class UserResponse(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None
    service: Optional[str] = None
    auth_provider: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            UUID4: str,
            datetime: lambda dt: dt.isoformat()
        }

# Update forward refs after all classes are defined
AuthResponse.update_forward_refs()


