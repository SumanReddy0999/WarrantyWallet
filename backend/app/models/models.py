import uuid
from sqlalchemy import (
    create_engine,
    Column,
    String,
    DateTime,
    Date,
    ForeignKey,
    Enum,
    Integer
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

# Vector support removed

# Base class for all models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    phone = Column(String(50), unique=True, nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    service = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    auth_provider = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    warranties = relationship("Warranty", back_populates="user", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    categories_name = Column(String, unique=True, nullable=False)

    warranties = relationship("Warranty", back_populates="category")

class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manufaturer_name = Column(String, nullable=False, unique=True)
    contact_info = Column(JSONB)
    phone_num = Column(String(20))
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    products = relationship("Product", back_populates="manufacturer", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    manufacturer_id = Column(UUID(as_uuid=True), ForeignKey("manufacturers.id", ondelete="CASCADE"), nullable=False)
    product_name = Column(String, nullable=False)
    model_number = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    manufacturer = relationship("Manufacturer", back_populates="products")
    warranties = relationship("Warranty", back_populates="product")

class Warranty(Base):
    __tablename__ = "warranties"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="SET NULL"))
    original_filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    file_mime_type = Column(String)
    upload_status = Column(String, default='processing', nullable=False)
    serial_number = Column(String)
    warranty_number = Column(String)
    purchase_date = Column(Date)
    expiry_date = Column(Date)
    retailer_name = Column(String)
    additional_metadata = Column(JSONB)
    uploaded_at = Column(DateTime,    server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="warranties")
    product = relationship("Product", back_populates="warranties")
    category = relationship("Category", back_populates="warranties")
    document_chunks = relationship("DocumentChunk", back_populates="warranty", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="warranty", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="warranty", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    warranty_id = Column(UUID(as_uuid=True), ForeignKey("warranties.id", ondelete="CASCADE"), nullable=False)
    chunk_text = Column(String, nullable=False)
    chunk_metadata = Column('metadata', JSONB)  # Using 'metadata' as the actual column name in the database
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    warranty = relationship("Warranty", back_populates="document_chunks")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    warranty_id = Column(UUID(as_uuid=True), ForeignKey("warranties.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="chat_sessions")
    warranty = relationship("Warranty", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    sender_type = Column(String, nullable=False)  # 'user' or 'ai'
    content = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    session = relationship("ChatSession", back_populates="messages")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    warranty_id = Column(UUID(as_uuid=True), ForeignKey("warranties.id", ondelete="CASCADE"), nullable=False)
    notification_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, default='created', nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="notifications")
    warranty = relationship("Warranty", back_populates="notifications")
