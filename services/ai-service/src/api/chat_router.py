import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.chat import ChatRequest, ChatResponse
from ..services.rag_graph_service import app as rag_app # Import the compiled graph
from ..db.database import get_db

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_warranty(
    request: ChatRequest,
    db: Session = Depends(get_db) # Keep DB session for potential future use
):
    """
    Handles a chat request for a specific warranty.
    """
    inputs = {
        "question": request.question,
        "warranty_id": request.warranty_id
    }
    
    # Invoke the RAG graph with the user's input
    final_state = rag_app.invoke(inputs)
    
    return ChatResponse(answer=final_state["generation"])