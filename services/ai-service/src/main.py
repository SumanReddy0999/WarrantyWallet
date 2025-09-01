from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import both routers
from .api.ingestion_router import router as ingestion_router
from .api.chat_router import router as chat_router
from .db.database import engine
from .db import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Warranty Wallet AI Service",
    description="Service for warranty document ingestion and RAG-based chat.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include both routers with distinct tags
app.include_router(ingestion_router, prefix="/api/ai", tags=["Ingestion"])
app.include_router(chat_router, prefix="/api/ai", tags=["Chat"])

@app.get("/", tags=["Root"])
def read_root():
    """A simple health check endpoint."""
    return {"message": "AI Service is running"}