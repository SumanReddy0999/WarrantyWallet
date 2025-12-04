from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.models import Product
from .base import BaseRepository

class ProductRepository(BaseRepository[Product, dict, dict]):
    """Repository for product operations"""
    
    def get_by_name(self, name: str) -> Optional[Product]:
        """Get a product by name (case-insensitive)"""
        return self.db_session.query(self.model)\
            .filter(Product.product_name.ilike(f"%{name}%"))\
            .first()
    
    def get_by_manufacturer(self, manufacturer_id: UUID) -> List[Product]:
        """Get all products for a manufacturer"""
        return self.db_session.query(self.model)\
            .filter(Product.manufacturer_id == manufacturer_id)\
            .all()
    
    def get_by_name_and_manufacturer(
        self, 
        name: str, 
        manufacturer_id: UUID
    ) -> Optional[Product]:
        """Get a product by name and manufacturer"""
        return self.db_session.query(self.model)\
            .filter(
                Product.product_name.ilike(f"%{name}%"),
                Product.manufacturer_id == manufacturer_id
            )\
            .first()
    
    def search(self, query: str, limit: int = 10) -> List[Product]:
        """Search products by name or model number"""
        return self.db_session.query(self.model)\
            .filter(
                (Product.product_name.ilike(f"%{query}%")) |
                (Product.model_number.ilike(f"%{query}%"))
            )\
            .limit(limit)\
            .all()
