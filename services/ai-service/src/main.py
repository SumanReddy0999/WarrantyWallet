from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import router as ai_router 
from .db.database import engine               
from .db import models                        

# This command ensures all tables are created if they don't exist.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Warranty RAG Ingestion Pipeline",
    description="Service for processing, extracting, and embedding warranty documents.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Allows frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router 
app.include_router(ai_router, prefix="/api/ai", tags=["AI Ingestion"])

# Root endpoint for health checks
@app.get("/")
def read_root():
    return {"message": "AI Service is running"}