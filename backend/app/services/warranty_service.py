from datetime import date, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.models import Warranty
from app.schemas.warranty import WarrantyCreate, WarrantyUpdate, WarrantyResponse
from app.repositories.warranty import WarrantyRepository
from app.repositories.product import ProductRepository
from app.repositories.manufacturer import ManufacturerRepository
from app.repositories.category import CategoryRepository

class WarrantyService:
    """Service for warranty business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.warranty_repo = WarrantyRepository(Warranty, db)
        self.product_repo = ProductRepository(Product, db)
        self.manufacturer_repo = ManufacturerRepository(Manufacturer, db)
        self.category_repo = CategoryRepository(Category, db)
    
    def get_warranty(self, warranty_id: UUID, user_id: UUID) -> Warranty:
        """Get a single warranty with authorization check"""
        warranty = self.warranty_repo.get(warranty_id)
        if not warranty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Warranty not found"
            )
        
        if warranty.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this warranty"
            )
            
        return warranty
    
    def get_user_warranties(
        self, 
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Warranty]:
        """Get warranties for a specific user"""
        return self.warranty_repo.get_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            filters=filters or {}
        )
    
    def create_warranty(
        self, 
        warranty_in: WarrantyCreate, 
        user_id: UUID
    ) -> Warranty:
        """Create a new warranty with related entities"""
        return self.warranty_repo.create_with_relations(warranty_in, user_id)
    
    def update_warranty(
        self, 
        warranty_id: UUID, 
        warranty_in: WarrantyUpdate, 
        user_id: UUID
    ) -> Warranty:
        """Update an existing warranty"""
        # First verify ownership
        warranty = self.get_warranty(warranty_id, user_id)
        
        # Update the warranty
        return self.warranty_repo.update(
            db_obj=warranty,
            obj_in=warranty_in.dict(exclude_unset=True)
        )
    
    def delete_warranty(self, warranty_id: UUID, user_id: UUID) -> Warranty:
        """Delete a warranty"""
        # Verify ownership
        warranty = self.get_warranty(warranty_id, user_id)
        
        # Delete the warranty
        return self.warranty_repo.remove(id=warranty_id)
    
    def get_expiring_warranties(
        self, 
        user_id: UUID, 
        days: int = 30
    ) -> List[Warranty]:
        """Get warranties expiring soon for a user"""
        # Get all user warranties
        warranties = self.get_user_warranties(user_id)
        
        # Filter for expiring soon
        today = date.today()
        expiration_date = today + timedelta(days=days)
        
        return [
            w for w in warranties 
            if w.expiry_date and today <= w.expiry_date <= expiration_date
        ]
    
    def get_warranty_stats(self, user_id: UUID) -> Dict[str, Any]:
        """Get statistics about user's warranties"""
        warranties = self.get_user_warranties(user_id)
        
        total = len(warranties)
        active = sum(1 for w in warranties if w.expiry_date and w.expiry_date >= date.today())
        expired = total - active
        
        # Count by category
        categories = {}
        for w in warranties:
            if w.category:
                cat_name = w.category.categories_name
                categories[cat_name] = categories.get(cat_name, 0) + 1
        
        return {
            "total": total,
            "active": active,
            "expired": expired,
            "by_category": categories
        }
