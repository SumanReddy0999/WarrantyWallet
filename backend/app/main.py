from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .db.database import create_tables, engine
from .routers import auth as auth_router
from .routers import ai as ai_router


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
    origins = [
        "http://localhost:5000",   # Backend port
        "http://127.0.0.1:5000",   # Backend port alternative
        "http://localhost:5173",   # Vite default port
        "http://localhost:5174",   # Common Vite alternative port
        "http://localhost:3000",   # Common React port
        "http://127.0.0.1:3000",   # Localhost alternative
        "http://127.0.0.1:5173",   # Localhost alternative
        "http://127.0.0.1:5174",   # Localhost alternative
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"]
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    app.include_router(auth_router.router)
    app.include_router(ai_router.router)
    return app


app = create_app()