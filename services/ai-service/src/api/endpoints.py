import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..db import operations as db_ops
from ..schemas.warranty import WarrantyProcessResponse
from ..services.structured_extractor import extract_data
from ..services.vector_store_handler import create_chunks_and_embeddings
from ..services.warranty_logic import process_and_validate_warranty_data
from ..core.config import TEMP_UPLOAD_DIR

router = APIRouter()

@router.post("/process-warranty", response_model=WarrantyProcessResponse)
async def process_warranty_pipeline(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Orchestrates the entire RAG ingestion pipeline.
    """
    os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)
    temp_path = os.path.join(TEMP_UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"INFO: File '{file.filename}' temporarily saved to '{temp_path}'.")

        extracted_data, raw_text = extract_data(temp_path)
        processed_data = process_and_validate_warranty_data(extracted_data)

        try:
            user_uuid = uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id format. Must be a valid UUID.")

        manufacturer = db_ops.get_or_create_manufacturer(db, name=processed_data.manufacturer, contact_info=processed_data.contact_info)
        product = db_ops.get_or_create_product(db, name=processed_data.product_name, model_number=processed_data.model_number, manufacturer_id=manufacturer.id)
        
        # New: Get or create the category
        category = db_ops.get_or_create_category(db, name=processed_data.category)
        
        warranty = db_ops.create_warranty_record(
            db, user_id=user_uuid, product_id=product.id,
            category_id=category.id, # Pass the category ID
            data=processed_data, filename=file.filename,
            storage_path=temp_path, mime_type=file.content_type
        )

        chunks_with_vectors = create_chunks_and_embeddings(raw_text, processed_data)
        if chunks_with_vectors:
            db_ops.add_document_chunks(db, warranty_id=warranty.id, chunks=chunks_with_vectors)

        db_ops.update_warranty_status(db, warranty_id=warranty.id, status='completed')

        return WarrantyProcessResponse(
            message="Warranty processed and ingested successfully.",
            warranty_id=warranty.id,
            data=processed_data
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print(f"FATAL ERROR in pipeline: {e}")
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"INFO: Cleaned up temporary file '{temp_path}'.")