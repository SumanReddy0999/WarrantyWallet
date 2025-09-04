from datetime import date, datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, UUID4
from .base import BaseSchema

class WarrantyBase(BaseSchema):
    category_id: Optional[UUID4] = Field(None, description="Category ID")
    product_id: Optional[UUID4] = Field(None, description="Product ID")
    serial_number: Optional[str] = Field(None, max_length=100, description="Product serial number")
    warranty_number: Optional[str] = Field(None, max_length=100, description="Warranty number")
    purchase_date: Optional[date] = Field(None, description="Purchase date")
    expiry_date: Optional[date] = Field(None, description="Warranty expiry date")
    retailer_name: Optional[str] = Field(None, max_length=200, description="Retailer name")
    additional_metadata: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional metadata in JSON format"
    )

class WarrantyCreate(WarrantyBase):
    original_filename: str = Field(..., description="Original file name")
    storage_path: str = Field(..., description="File storage path")
    file_mime_type: str = Field(..., description="File MIME type")

class WarrantyUpdate(WarrantyBase):
    upload_status: Optional[str] = Field(
        None, 
        description="Upload status (e.g., 'processing', 'completed')"
    )

class WarrantyResponse(WarrantyBase):
    id: UUID4
    user_id: UUID4
    original_filename: str
    storage_path: str
    file_mime_type: str
    upload_status: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class WarrantyListResponse(BaseModel):
    items: list[WarrantyResponse]
    total: int
    page: int
    size: int
