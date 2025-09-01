import uuid
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from . import models
from ..schemas.warranty import WarrantyData
from langsmith import traceable

@traceable(name="Initial DB Setup")
def setup_initial_records(
    db: Session,
    user_uuid: uuid.UUID,
    processed_data: WarrantyData,
    file_info: Dict[str, str]
) -> models.Warranty:
    """
    Creates the primary records (manufacturer, product, category, warranty)
    and returns the main warranty object.
    """
    manufacturer = get_or_create_manufacturer(db, name=processed_data.manufacturer, contact_info=processed_data.contact_info)
    product = get_or_create_product(db, name=processed_data.product_name, model_number=processed_data.model_number, manufacturer_id=manufacturer.id)
    category = get_or_create_category(db, name=processed_data.category)
    
    warranty = create_warranty_record(
        db, user_id=user_uuid, product_id=product.id,
        category_id=category.id,
        data=processed_data, filename=file_info['filename'],
        storage_path=file_info['storage_path'], mime_type=file_info['mime_type']
    )
    return warranty

@traceable(name="Final DB Commits")
def finalize_ingestion(
    db: Session,
    warranty_id: uuid.UUID,
    #chunks_with_vectors: List[Dict[str, Any]]
):
    """
    Adds document chunks and updates the final warranty status.
    """
    '''
    if chunks_with_vectors:
        add_document_chunks(db, warranty_id=warranty_id, chunks=chunks_with_vectors)
        '''

    update_warranty_status(db, warranty_id=warranty_id, status='completed')


# --- Individual DB functions (remain as child runs) ---

@traceable
def get_or_create_category(db: Session, name: str) -> models.Category:
    # ... (function content remains the same)
    if not name or not name.strip():
        name = "Other"
    category = db.query(models.Category).filter(models.Category.name == name).first()
    if not category:
        category = models.Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

@traceable
def get_or_create_manufacturer(db: Session, name: str, contact_info: str | None) -> models.Manufacturer:
    # ... (function content remains the same)
    manufacturer = db.query(models.Manufacturer).filter(models.Manufacturer.name == name).first()
    if not manufacturer:
        manufacturer = models.Manufacturer(
            name=name,
            contact_info={"details": contact_info} if contact_info else {}
        )
        db.add(manufacturer)
        db.commit()
        db.refresh(manufacturer)
    return manufacturer

@traceable
def get_or_create_product(db: Session, name: str, model_number: str | None, manufacturer_id: uuid.UUID) -> models.Product:
    # ... (function content remains the same)
    product = db.query(models.Product).filter_by(
        name=name,
        model_number=model_number,
        manufacturer_id=manufacturer_id
    ).first()
    if not product:
        product = models.Product(
            name=name,
            model_number=model_number,
            manufacturer_id=manufacturer_id
        )
        db.add(product)
        db.commit()
        db.refresh(product)
    return product

@traceable
def create_warranty_record(
    db: Session,
    user_id: uuid.UUID,
    product_id: uuid.UUID,
    category_id: uuid.UUID | None,
    data: WarrantyData,
    filename: str,
    storage_path: str,
    mime_type: str | None
) -> models.Warranty:
    # ... (function content remains the same)
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

'''
@traceable
def add_document_chunks(db: Session, warranty_id: uuid.UUID, chunks: List[Dict[str, Any]]):
    # ... (function content remains the same)
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
    '''

@traceable
def update_warranty_status(db: Session, warranty_id: uuid.UUID, status: str) -> models.Warranty:
    # ... (function content remains the same)
    warranty = db.query(models.Warranty).filter(models.Warranty.id == warranty_id).first()
    if warranty:
        warranty.upload_status = status
        db.commit()
        db.refresh(warranty)
    return warranty