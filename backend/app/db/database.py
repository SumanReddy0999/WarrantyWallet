from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from app.core.config import settings

# Create database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models after engine is created to ensure they are registered with SQLAlchemy
from app.models.models import Base

def get_db():
    """Dependency to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    # Create a new connection to avoid any transaction issues
    with engine.connect() as connection:
        # Start a new transaction
        trans = connection.begin()
        try:
            # Drop all tables first (be careful with this in production!)
            Base.metadata.drop_all(bind=connection)
            # Create all tables
            Base.metadata.create_all(bind=connection)
            trans.commit()
            print("✅ Database tables created successfully")
        except Exception as e:
            trans.rollback()
            print(f"❌ Error creating database tables: {e}")
            raise

# Initialize database tables when this module is imported
if __name__ == "__main__":
    create_tables()
