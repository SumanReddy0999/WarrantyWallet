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
from langchain_postgres.vectorstores import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document
from ..core.config import TEMP_UPLOAD_DIR, EMBEDDING_MODEL_NAME, GEMINI_API_KEY, DATABASE_URL
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

        # Step 1: Data Extraction and Validation
        extracted_data, raw_text = extract_data(temp_path)
        processed_data = process_and_validate_warranty_data(extracted_data)
        
        # Step 2: Initial Database Setup
        file_info = {
            "filename": file.filename,
            "storage_path": temp_path,
            "mime_type": file.content_type
        }
        user_uuid = uuid.UUID(user_id)
        warranty = db_ops.setup_initial_records(
            db=db,
            user_uuid=user_uuid,
            processed_data=processed_data,
            file_info=file_info
        )
        
        # Step 3: Chunking and Embedding (now with the required warranty.id)
        chunks_data = create_chunks_and_embeddings(raw_text, processed_data, warranty.id)

        documents = [Document(page_content=chunk["text"], metadata=chunk["chunk_metadata"]) for chunk in chunks_data]
        # Step 4: Add Documents to LangChain-Managed Vector Store
        if documents:
            embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL_NAME, google_api_key= GEMINI_API_KEY)
            PGVector.from_documents(
                embedding=embeddings,
                documents=documents,
                collection_name=str(warranty.id), # Use warranty.id as a unique collection name
                connection=DATABASE_URL,
            )
            print(f"INFO: Added {len(documents)} chunks to vector store for warranty {warranty.id}")

        # Step 5: Final Database Commits
        db_ops.finalize_ingestion(
            db=db,
            warranty_id=warranty.id,
            
        )
        
        return warranty.id, processed_data

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)