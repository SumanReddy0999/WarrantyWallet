import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    JSON,
    DateTime,
    Uuid,
    Integer,
    Date,
    ForeignKey,
    func,
    Identity
)
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector
from ..core.config import EMBEDDING_DIMENSION

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Identity(start=1, cycle=False), primary_key=True)
    name = Column(String, nullable=False, unique=True)

class Manufacturer(Base):
    __tablename__ = 'manufacturers'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    contact_info = Column("contact_info", JSON)
    created_at = Column("created_at", DateTime, server_default=func.now(), nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    manufacturer_id = Column("manufacturer_id", Uuid, ForeignKey('manufacturers.id', ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    model_number = Column("model_number", String)
    created_at = Column("created_at", DateTime, server_default=func.now(), nullable=False)

class Warranty(Base):
    __tablename__ = 'warranties'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id = Column("user_id", Uuid, nullable=False, index=True)
    category_id = Column("category_id", Integer, ForeignKey('categories.id'), index=True)
    product_id = Column("product_id", Uuid, ForeignKey('products.id', ondelete="SET NULL"))
    original_filename = Column("original_filename", String, nullable=False)
    storage_path = Column("storage_path", String, nullable=False)
    file_mime_type = Column("file_mime_type", String)
    upload_status = Column("upload_status", String, default='processing', nullable=False)
    serial_number = Column("serial_number", String)
    warranty_number = Column("warranty_number", String)
    purchase_date = Column("purchase_date", Date)
    expiry_date = Column("expiry_date", Date)
    retailer_name = Column("retailer_name", String)
    additional_metadata = Column("additional_metadata", JSON)
    uploaded_at = Column("uploaded_at", DateTime, server_default=func.now(), nullable=False)

class DocumentChunk(Base):
    __tablename__ = 'document_chunks'
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    warranty_id = Column("warranty_id", Uuid, ForeignKey('warranties.id', ondelete="CASCADE"), nullable=False, index=True)
    chunk_text = Column("chunk_text", Text, nullable=False)
    vector = Column(Vector(EMBEDDING_DIMENSION))
    chunk_metadata = Column("metadata", JSON)
    created_at = Column("created_at", DateTime, server_default=func.now(), nullable=False)