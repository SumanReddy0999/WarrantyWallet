import os
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from pathlib import Path

from .core.config import settings
from .db.database import create_tables, engine
from .routers import auth as auth_router
from .routers import ai as ai_router
from .routers import warranties as warranties_router
from app.core.security import get_current_user
from app.models.models import User

def create_app() -> FastAPI:
    # Create database tables on startup
    create_tables()

    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version="1.0.0",
        description="Warranty Wallet API Service"
    )
    
    # CORS middleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=600
    )
    
    # Create uploads directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Serve static files
    app.mount("/uploads", StaticFiles(directory=upload_dir), name="uploads")

    @app.get("/health")
    def health(current_user: User = Depends(get_current_user)):
        return {"status": "ok"}

    # Swagger OAuth2 (Bearer Token)
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
    
    # Custom OpenAPI to enable global Bearer Auth
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Add global Bearer Token security
        openapi_schema["components"]["securitySchemes"] = {
            "OAuth2PasswordBearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }

        
        openapi_schema["security"] = [
            {"OAuth2PasswordBearer": []}
        ]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    # Include routers
    app.include_router(auth_router.router, prefix="/api")
    app.include_router(ai_router.router, prefix="/api")
    app.include_router(warranties_router.router, prefix="/api")
    
    return app


app = create_app()
