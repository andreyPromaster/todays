from typing import Any, Generic, List, Optional, Type, TypeVar

from crud.base import ModelType
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import Session

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseMixin:
    def __init__(self, model: Type[ModelType]):
        self.model = model


class RetrieveModelMixin(BaseMixin):
    """
    Get a model instance and a list of model instances
    """

    def get(self, obj_id: Any, db: Session) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def get_by_any_field(
        self, db: Session, field_name: str, field_value: str
    ) -> Optional[ModelType]:
        filters = {field_name: field_value}
        if field_name in [column.name for column in inspect(self.model).c]:
            return db.query(self.model).filter_by(**filters).first()

    def list(
        self,
        db: Session,
        skip: int,
        limit: int,
        filters: Optional[dict] = None,
        ordering: Optional[list] = None,
    ) -> List[ModelType]:
        if filters is not None:
            filters_keys = list(filters.keys())
            for key in filters_keys:
                if key not in [column.name for column in inspect(self.model).c]:
                    filters.pop(key)
        else:
            filters = {}

        if ordering is not None:
            for field in ordering:
                if field not in [column.name for column in inspect(self.model).c]:
                    ordering.remove(field)
        else:
            ordering = []

        return (
            db.query(self.model)
            .filter_by(**filters)
            .order_by(*ordering)
            .offset(skip)
            .limit(limit)
            .all()
        )


class CreateModelMixin(BaseMixin, Generic[CreateSchemaType]):
    """
    Create a model instance
    """

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj = self.model(**obj_in_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


class UpdateModelMixin(BaseMixin, Generic[UpdateSchemaType]):
    """
    Update a model instance
    """

    def update(self, db: Session, update_data: UpdateSchemaType, obj_db: ModelType) -> ModelType:
        update_data = jsonable_encoder(update_data)

        for field in update_data:
            if update_data.get(field):
                setattr(obj_db, field, update_data[field])

        db.add(obj_db)
        db.commit()
        db.refresh(obj_db)
        return obj_db


class DeleteModelMixin(BaseMixin):
    """
    Delete a model instance
    """

    def remove(self, db: Session, obj_id: Any) -> ModelType:
        obj = db.query(self.model).get(obj_id)
        db.delete(obj)
        db.commit()
        return obj
