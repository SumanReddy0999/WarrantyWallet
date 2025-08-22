import os
import shutil
import uuid
from sqlalchemy.orm import Session
from fastapi import UploadFile

from ..db import operations as db_ops
from ..schemas.warranty import WarrantyData
from .structured_extractor import extract_data
from .vector_store_handler import create_chunks_and_embeddings
from .warranty_logic import process_and_validate_warranty_data
from ..core.config import TEMP_UPLOAD_DIR
from langsmith import traceable

@traceable(name="Full Ingestion Pipeline")
def run_ingestion_pipeline(
    file: UploadFile,
    user_id: str,
    db: Session
) -> (uuid.UUID, WarrantyData):
    """
    This is the main orchestrator function that runs the entire pipeline
    and serves as the parent trace in LangSmith.
    """
    temp_path = os.path.join(TEMP_UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: Data Extraction and Processing
        extracted_data, raw_text = extract_data(temp_path)
        processed_data = process_and_validate_warranty_data(extracted_data)
        
        # Step 2: Chunking and Embedding
        chunks_with_vectors = create_chunks_and_embeddings(raw_text, processed_data)

        # Step 3: All Database Operations
        file_info = {
            "filename": file.filename,
            "storage_path": temp_path,
            "mime_type": file.content_type
        }
        user_uuid = uuid.UUID(user_id)
        
        # This single call will create the "Database Operations" parent run
        warranty = db_ops.persist_warranty_data(
            db=db,
            user_uuid=user_uuid,
            processed_data=processed_data,
            chunks_with_vectors=chunks_with_vectors,
            file_info=file_info
        )
        
        return warranty.id, processed_data

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)