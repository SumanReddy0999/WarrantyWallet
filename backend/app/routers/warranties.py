import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import os

from app.db.database import get_db
from app.models.models import User
from app.schemas.warranty import WarrantyCreate, WarrantyUpdate, WarrantyResponse, WarrantyListResponse
from app.services.warranty_service import WarrantyService
from app.services.file_service import FileService
from app.services.document_processor import DocumentProcessor
# Import authentication
from app.core.security import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/warranties", tags=["warranties"])

# Initialize services
def get_warranty_service(db: Session = Depends(get_db)) -> WarrantyService:
    return WarrantyService(db)

def get_file_service() -> FileService:
    return FileService(upload_dir=settings.UPLOAD_DIR)

def get_document_processor() -> DocumentProcessor:
    return DocumentProcessor(api_key=settings.GEMINI_API_KEY)

@router.get("/", response_model=WarrantyListResponse)
def list_warranties(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[UUID] = None,
    product_id: Optional[UUID] = None,
    status: Optional[str] = None,
    expires_soon: bool = False,
    current_user: User = Depends(get_current_user),
    warranty_service: WarrantyService = Depends(get_warranty_service)
):
    """
    List all warranties for the current user with optional filtering
    """
    filters = {}
    if category_id:
        filters['category_id'] = category_id
    if product_id:
        filters['product_id'] = product_id
    if status:
        filters['status'] = status
    if expires_soon:
        filters['expires_soon'] = True
    
    warranties = warranty_service.get_user_warranties(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        filters=filters
    )
    
    return {
        "items": warranties,
        "total": len(warranties),
        "page": skip // limit + 1,
        "size": limit
    }

@router.post("/", response_model=WarrantyResponse, status_code=status.HTTP_201_CREATED)
async def create_warranty(
    warranty_in: WarrantyCreate,
    current_user: User = Depends(get_current_user),
    warranty_service: WarrantyService = Depends(get_warranty_service)
):
    """
    Create a new warranty
    """
    return warranty_service.create_warranty(warranty_in, current_user.id)

# Configure file size limits
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload", response_model=WarrantyResponse, status_code=status.HTTP_201_CREATED)
async def upload_warranty_document(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service),
    doc_processor: DocumentProcessor = Depends(get_document_processor),
    db: Session = Depends(get_db)
):
    """
    Upload a warranty document and extract information
    """
    from app.core.config import settings
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting file upload for user {current_user.id}")
    
    # File size validation
    content_length = int(request.headers.get('content-length', 0))
    if content_length > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error": "File too large",
                "max_size": MAX_FILE_SIZE,
                "size_unit": "bytes",
                "max_size_mb": MAX_FILE_SIZE / (1024 * 1024)
            }
        )
        
    # Check file extension
    file_extension = Path(file.filename).suffix.lower()
    allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg", ".docx"}
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Invalid file type",
                "allowed_types": list(allowed_extensions)
            }
        )
    
    try:
        # Ensure upload directory exists and is writable
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        if not os.access(upload_dir, os.W_OK):
            logger.error(f"Upload directory is not writable: {upload_dir}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Server configuration error: Upload directory is not writable"
            )
            
        logger.info(f"Saving uploaded file: {file.filename}")
        
        # Save the uploaded file
        file_path, mime_type = await file_service.save_upload_file(file)
        logger.info(f"File saved to {file_path} with mime type {mime_type}")
        
        # Extract information from the document
        logger.info("Extracting warranty information from document...")
        extracted_data = await doc_processor.extract_warranty_info(file_path, mime_type)
        logger.info(f"Extracted data: {extracted_data}")
        
        # Create warranty from extracted data
        warranty_service = WarrantyService(db)
        
        # Map extracted data to WarrantyCreate schema
        warranty_in = WarrantyCreate(
            original_filename=file.filename,
            storage_path=str(file_path),
            file_mime_type=mime_type,
            serial_number=extracted_data.get('serial_number'),
            purchase_date=extracted_data.get('purchase_date'),
            expiry_date=extracted_data.get('expiry_date'),
            retailer_name=extracted_data.get('retailer_name'),
            additional_metadata={"extracted_data": extracted_data}
        )
        
        # If product info was extracted, include it
        if 'product_name' in extracted_data:
            from app.schemas.product import ProductCreate
            warranty_in.product = ProductCreate(
                product_name=extracted_data['product_name'],
                model_number=extracted_data.get('model_number'),
                manufacturer_name=extracted_data.get('manufacturer_name')
            )
        
        # If category was extracted, include it
        if 'category_name' in extracted_data:
            warranty_in.category_name = extracted_data['category_name']
        
        return warranty_service.create_warranty(warranty_in, current_user.id)
        
    except HTTPException as he:
        logger.error(f"HTTP error during file upload: {str(he)}")
        raise he
    except Exception as e:
        # Log the full error for debugging
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Error during file upload: {str(e)}\n{error_details}")
        
        # Clean up the file if it was created
        if 'file_path' in locals() and file_path and file_path.exists():
            try:
                file_service.delete_file(str(file_path))
                logger.info(f"Cleaned up file: {file_path}")
            except Exception as cleanup_error:
                logger.error(f"Error during file cleanup: {str(cleanup_error)}")
        
        # Return a more detailed error message for client
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing your request: {str(e)}"
        )

@router.get("/{warranty_id}", response_model=WarrantyResponse)
def get_warranty(
    warranty_id: UUID,
    current_user: User = Depends(get_current_user),
    warranty_service: WarrantyService = Depends(get_warranty_service)
):
    """
    Get a specific warranty by ID
    """
    return warranty_service.get_warranty(warranty_id, current_user.id)

@router.put("/{warranty_id}", response_model=WarrantyResponse)
def update_warranty(
    warranty_id: UUID,
    warranty_in: WarrantyUpdate,
    current_user: User = Depends(get_current_user),
    warranty_service: WarrantyService = Depends(get_warranty_service)
):
    """
    Update a warranty
    """
    return warranty_service.update_warranty(warranty_id, warranty_in, current_user.id)

@router.delete("/{warranty_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warranty(
    warranty_id: UUID,
    current_user: User = Depends(get_current_user),
    warranty_service: WarrantyService = Depends(get_warranty_service)
):
    """
    Delete a warranty
    """
    warranty_service.delete_warranty(warranty_id, current_user.id)
    return None

@router.get("/stats/")
def get_warranty_stats(
    current_user: User = Depends(get_current_user),
    warranty_service: WarrantyService = Depends(get_warranty_service)
):
    """
    Get statistics about user's warranties
    """
    return warranty_service.get_warranty_stats(current_user.id)

@router.get("/{warranty_id}/document")
def download_warranty_document(
    warranty_id: UUID,
    current_user: User = Depends(get_current_user),
    warranty_service: WarrantyService = Depends(get_warranty_service)
):
    """
    Download the original warranty document
    """
    warranty = warranty_service.get_warranty(warranty_id, current_user.id)
    
    if not os.path.exists(warranty.storage_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return FileResponse(
        warranty.storage_path,
        filename=warranty.original_filename,
        media_type=warranty.file_mime_type or "application/octet-stream"
    )
