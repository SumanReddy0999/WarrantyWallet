import uuid
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from . import models
from ..schemas.warranty import WarrantyData

def get_or_create_category(db: Session, name: str) -> models.Category:
    """Retrieves a category by name or creates it if it doesn't exist."""
    if not name or not name.strip():
        name = "Other"
        
    category = db.query(models.Category).filter(models.Category.name == name).first()
    if not category:
        print(f"INFO: Category '{name}' not found. Creating new record.")
        category = models.Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

def get_or_create_manufacturer(db: Session, name: str, contact_info: str | None) -> models.Manufacturer:
    """Retrieves a manufacturer by name or creates it if it doesn't exist."""
    manufacturer = db.query(models.Manufacturer).filter(models.Manufacturer.name == name).first()
    if not manufacturer:
        print(f"INFO: Manufacturer '{name}' not found. Creating new record.")
        manufacturer = models.Manufacturer(
            name=name,
            contact_info={"details": contact_info} if contact_info else {}
        )
        db.add(manufacturer)
        db.commit()
        db.refresh(manufacturer)
    return manufacturer

def get_or_create_product(db: Session, name: str, model_number: str | None, manufacturer_id: uuid.UUID) -> models.Product:
    """Retrieves a product by its details or creates it if it doesn't exist."""
    product = db.query(models.Product).filter_by(
        name=name,
        model_number=model_number,
        manufacturer_id=manufacturer_id
    ).first()
    if not product:
        print(f"INFO: Product '{name}' not found. Creating new record.")
        product = models.Product(
            name=name,
            model_number=model_number,
            manufacturer_id=manufacturer_id
        )
        db.add(product)
        db.commit()
        db.refresh(product)
    return product

def create_warranty_record(
    db: Session,
    user_id: uuid.UUID,
    product_id: uuid.UUID,
    category_id: int | None,
    data: WarrantyData,
    filename: str,
    storage_path: str,
    mime_type: str | None
) -> models.Warranty:
    """Creates a new warranty record in the database."""
    print("INFO: Creating new warranty record in the database.")
    warranty = models.Warranty(
        user_id=user_id,
        product_id=product_id,
        category_id=category_id,
        original_filename=filename,
        storage_path=storage_path,
        file_mime_type=mime_type,
        upload_status='processing',
        serial_number=data.serial_number,
        purchase_date=data.purchase_date,
        expiry_date=data.expiry_date,
        retailer_name=data.retailer_name,
        additional_metadata=data.model_dump(mode='json')
    )
    db.add(warranty)
    db.commit()
    db.refresh(warranty)
    return warranty

def add_document_chunks(db: Session, warranty_id: uuid.UUID, chunks: List[Dict[str, Any]]):
    """Bulk inserts document chunks into the database for a given warranty."""
    print(f"INFO: Bulk inserting {len(chunks)} document chunks into the database.")
    db_chunks = [
        models.DocumentChunk(
            warranty_id=warranty_id,
            chunk_text=chunk_data['text'],
            vector=chunk_data['vector'],
            chunk_metadata=chunk_data['chunk_metadata']
        ) for chunk_data in chunks
    ]
    db.bulk_save_objects(db_chunks)
    db.commit()
    print("SUCCESS: Document chunks inserted.")

def update_warranty_status(db: Session, warranty_id: uuid.UUID, status: str) -> models.Warranty:
    """Updates the status of a warranty record."""
    warranty = db.query(models.Warranty).filter(models.Warranty.id == warranty_id).first()
    if warranty:
        print(f"INFO: Updating warranty {warranty_id} status to '{status}'.")
        warranty.upload_status = status
        db.commit()
        db.refresh(warranty)
        return warranty
    return None