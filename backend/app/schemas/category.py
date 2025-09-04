from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the category")
    description: str | None = Field(None, max_length=500, description="Category description")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: str | None = Field(None, max_length=100, description="Name of the category")
    description: str | None = Field(None, max_length=500, description="Category description")

class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
