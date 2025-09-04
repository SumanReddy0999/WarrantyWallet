from pydantic import BaseModel, Field, UUID4
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    product_name: str = Field(..., max_length=200, description="Name of the product")
    model_number: Optional[str] = Field(None, max_length=100, description="Model number")
    manufacturer_id: UUID4 = Field(..., description="ID of the manufacturer")
    
    class Config:
        protected_namespaces = ()  # Resolves the 'model_' namespace conflict

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    product_name: Optional[str] = Field(None, max_length=200, description="Name of the product")
    model_number: Optional[str] = Field(None, max_length=100, description="Model number")
    manufacturer_id: Optional[UUID4] = Field(None, description="ID of the manufacturer")

class ProductResponse(ProductBase):
    id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True
