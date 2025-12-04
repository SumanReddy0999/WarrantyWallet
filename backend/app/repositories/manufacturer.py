
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.models import Manufacturer
from .base import BaseRepository

class ManufacturerRepository(BaseRepository[Manufacturer, dict, dict]):
    """Repository for manufacturer operations"""
    
    def get_by_name(self, name: str) -> Optional[Manufacturer]:
        """Get a manufacturer by name (case-insensitive)"""
        return self.db_session.query(self.model)\
            .filter(Manufacturer.manufacturer_name.ilike(f"%{name}%"))\
            .first()
    
    def search(self, query: str, limit: int = 10) -> List[Manufacturer]:
        """Search manufacturers by name"""
        return self.db_session.query(self.model)\
            .filter(Manufacturer.manufacturer_name.ilike(f"%{query}%"))\
            .limit(limit)\
            .all()
    
    def get_with_products(self, manufacturer_id: UUID) -> Optional[Manufacturer]:
        """Get a manufacturer with its products"""
        from sqlalchemy.orm import joinedload
        return self.db_session.query(self.model)\
            .options(joinedload(Manufacturer.products))\
            .filter(Manufacturer.id == manufacturer_id)\
            .first()
