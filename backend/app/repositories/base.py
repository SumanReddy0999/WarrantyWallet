from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=dict)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=dict)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base repository with default CRUD operations"""

    def __init__(self, model: Type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session

    def get(self, id: Union[UUID, str]) -> Optional[ModelType]:
        """Get a single model by ID"""
        return self.db_session.get(self.model, id)

    def get_multi(
        self, *, skip: int = 0, limit: int = 100, **filters: Any
    ) -> List[ModelType]:
        """Get multiple models with optional filtering"""
        stmt = select(self.model).offset(skip).limit(limit)
        if filters:
            stmt = stmt.filter_by(**filters)
        return list(self.db_session.scalars(stmt).all())

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new model"""
        db_obj = self.model(**obj_in)
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj

    def update(
        self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update a model"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj

    def remove(self, *, id: Union[UUID, str]) -> ModelType:
        """Remove a model"""
        obj = self.db_session.get(self.model, id)
        self.db_session.delete(obj)
        self.db_session.commit()
        return obj
