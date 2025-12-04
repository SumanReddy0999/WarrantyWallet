from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.models import Category
from .base import BaseRepository

class CategoryRepository(BaseRepository[Category, dict, dict]):
    """Repository for category operations"""
    
    def get_by_name(self, name: str) -> Optional[Category]:
        """Get a category by name (case-insensitive)"""
        return self.db_session.query(self.model)\
            .filter(Category.categories_name.ilike(f"%{name}%"))\
            .first()
    
    def search(self, query: str, limit: int = 10) -> List[Category]:
        """Search categories by name"""
        return self.db_session.query(self.model)\
            .filter(Category.categories_name.ilike(f"%{query}%"))\
            .limit(limit)\
            .all()
    
    def get_with_warranties(self, category_id: UUID) -> Optional[Category]:
        """Get a category with its warranties"""
        from sqlalchemy.orm import joinedload
        return self.db_session.query(self.model)\
            .options(joinedload(Category.warranties))\
            .filter(Category.id == category_id)\
            .first()
