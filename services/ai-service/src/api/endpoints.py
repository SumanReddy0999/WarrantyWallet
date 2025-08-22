import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.warranty import WarrantyProcessResponse

from ..services.pipeline_orchestrator import run_ingestion_pipeline

router = APIRouter()

@router.post("/process-warranty", response_model=WarrantyProcessResponse)
async def process_warranty_pipeline(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Handles the web request and calls the main orchestrator function.
    """
    try:
        # Validate UUID format before calling the pipeline
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user_id format. Must be a valid UUID.")

        # Call the single, traceable orchestrator function
        warranty_id, processed_data = run_ingestion_pipeline(file, user_id, db)

        return WarrantyProcessResponse(
            message="Warranty processed and ingested successfully.",
            warranty_id=warranty_id,
            data=processed_data
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print(f"FATAL ERROR in pipeline: {e}")
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")