from pydantic import BaseModel, Field
from typing import Optional
import uuid
import datetime

class WarrantyData(BaseModel):
    """
    Pydantic model for the structured data to be extracted from a warranty document.
    This structure is used by the LLM for parsing and by the application for validation.
    """
    manufacturer: Optional[str] = Field(
        None, description="The name of the company that manufactured or sold the product (e.g., 'HP', 'NovaTech Electronics Pvt. Ltd.', 'Kanak Enterprises')."
    )
    product_name: Optional[str] = Field(
        None, description="The primary name or description of the product (e.g., 'NovaSound X5 Wireless Speaker', 'ULTRADART USB Type C Cable')."
    )
    model_number: Optional[str] = Field(
        None, description="The model number of the product, if available (e.g., 'NSX5-BLK', '4SC12PA')."
    )
    serial_number: Optional[str] = Field(
        None, description="The serial number of the product, if available."
    )
    purchase_date: Optional[datetime.date] = Field(
        None, description="The date the product was purchased or ordered, converted to YYYY-MM-DD format."
    )
    warranty_period: Optional[str] = Field(
        None, description="The stated duration of the warranty (e.g., '2 Years', '6 months', '3 Months')."
    )
    expiry_date: Optional[datetime.date] = Field(
        None, description="The date the warranty expires, converted to YYYY-MM-DD format."
    )
    retailer_name: Optional[str] = Field(
        None, description="The name of the retailer or 'Sold By' entity if different from the manufacturer (e.g., 'Appario Retail Private Ltd', 'Flipkart')."
    )
    contact_info: Optional[str] = Field(
        None, description="The customer support contact information (phone, email, or website)."
    )
    category: Optional[str] = Field(
        None, description="Classify the product into one of the following categories: Electronics, Appliances, Clothing, Vehicles, Tools, Furniture, Other."
    )
class WarrantyProcessResponse(BaseModel):
    """Pydantic model for the final, successful API response."""
    message: str
    warranty_id: uuid.UUID 
    data: WarrantyData