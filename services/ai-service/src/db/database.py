from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import DATABASE_URL

# Create a SQLAlchemy engine instance.
# pool_pre_ping=True handles cases where the database connection might be stale.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function for FastAPI to get a database session for each request.
    This ensures the session is always closed after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()