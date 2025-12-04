from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from datetime import date

from app.models.models import Warranty, Product, Manufacturer, Category
from app.schemas.warranty import WarrantyCreate, WarrantyUpdate
from .base import BaseRepository

class WarrantyRepository(BaseRepository[Warranty, WarrantyCreate, WarrantyUpdate]):
    """Repository for warranty operations"""
    
    def get_by_user(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Warranty]:
        """Get warranties for a specific user with optional filtering"""
        query = self.db_session.query(self.model).filter(
            self.model.user_id == user_id
        )
        
        if filters:
            if 'category_id' in filters:
                query = query.filter(self.model.category_id == filters['category_id'])
            if 'product_id' in filters:
                query = query.filter(self.model.product_id == filters['product_id'])
            if 'status' in filters:
                query = query.filter(self.model.status == filters['status'])
            if 'expires_soon' in filters and filters['expires_soon']:
                # Filter warranties expiring in the next 30 days
                from sqlalchemy import and_
                from datetime import datetime, timedelta
                
                thirty_days_later = datetime.utcnow() + timedelta(days=30)
                query = query.filter(
                    and_(
                        self.model.expiry_date >= datetime.utcnow().date(),
                        self.model.expiry_date <= thirty_days_later.date()
                    )
                )
        
        return query.offset(skip).limit(limit).all()
    
    def get_with_relations(self, warranty_id: UUID) -> Optional[Warranty]:
        """Get a warranty with all its relations loaded"""
        return self.db_session.query(self.model)\
            .options(
                joinedload(self.model.product)\
                .joinedload(Product.manufacturer),
                joinedload(self.model.category)
            )\
            .filter(self.model.id == warranty_id)\
            .first()
    
    def get_expiring_soon(self, days: int = 30) -> List[Warranty]:
        """Get warranties expiring soon"""
        from datetime import date, timedelta
        
        expiration_date = date.today() + timedelta(days=days)
        return self.db_session.query(self.model)\
            .filter(
                self.model.expiry_date.between(
                    date.today(),
                    expiration_date
                )
            )\
            .all()
    
    def create_with_relations(
        self, 
        obj_in: WarrantyCreate,
        user_id: UUID
    ) -> Warranty:
        """Create a warranty with related entities"""
        from app.repositories.product import ProductRepository
        from app.repositories.manufacturer import ManufacturerRepository
        from app.repositories.category import CategoryRepository
        
        db_obj = self.model(
            user_id=user_id,
            original_filename=obj_in.original_filename,
            storage_path=obj_in.storage_path,
            file_mime_type=obj_in.file_mime_type,
            serial_number=obj_in.serial_number,
            warranty_number=obj_in.warranty_number,
            purchase_date=obj_in.purchase_date,
            expiry_date=obj_in.expiry_date,
            retailer_name=obj_in.retailer_name,
            additional_metadata=obj_in.additional_metadata
        )
        
        # Handle product and manufacturer
        if obj_in.product_id:
            db_obj.product_id = obj_in.product_id
        elif hasattr(obj_in, 'product') and obj_in.product:
            # Create or get manufacturer
            manufacturer_repo = ManufacturerRepository(Manufacturer, self.db_session)
            manufacturer = manufacturer_repo.get_by_name(obj_in.product.manufacturer_name)
            if not manufacturer:
                manufacturer = manufacturer_repo.create({
                    'manufacturer_name': obj_in.product.manufacturer_name,
                    'contact_info': obj_in.product.manufacturer_contact_info
                })
            
            # Create or get product
            product_repo = ProductRepository(Product, self.db_session)
            product = product_repo.get_by_name_and_manufacturer(
                obj_in.product.product_name,
                manufacturer.id
            )
            if not product:
                product_data = {
                    'manufacturer_id': manufacturer.id,
                    'product_name': obj_in.product.product_name,
                    'model_number': obj_in.product.model_number
                }
                product = product_repo.create(product_data)
            
            db_obj.product_id = product.id
        
        # Handle category
        if obj_in.category_id:
            db_obj.category_id = obj_in.category_id
        elif hasattr(obj_in, 'category_name') and obj_in.category_name:
            category_repo = CategoryRepository(Category, self.db_session)
            category = category_repo.get_by_name(obj_in.category_name)
            if not category:
                category = category_repo.create({
                    'categories_name': obj_in.category_name
                })
            db_obj.category_id = category.id
        
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj
