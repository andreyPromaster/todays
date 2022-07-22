from typing import Any, Generic, List, Optional, TypeVar

from crud.base import ModelType
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import Session, load_only

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class HandlerMixin:
    @property
    def model_fields(self):
        """return all self model fields metadata"""
        return inspect(self.model).c

    def field_exists(self, field_name: str):
        return field_name in self.model_fields.keys()

    def field_is_unique(self, field_name: str):
        return (
            self.model_fields.get(field_name).primary_key
            or self.model_fields.get(field_name).unique
        )

    def init_get_list_parameters(
        self,
        filters: Optional[dict] = None,
        ordering: Optional[list] = None,
        select_fields: Optional[list] = None,
    ):
        if filters is not None:
            for field in filters.keys():
                if not self.field_exists(field):
                    filters.pop(field)
        else:
            filters = {}

        if ordering is not None:
            for field in ordering:
                if not self.field_exists(field):
                    ordering.remove(field)
        else:
            ordering = []

        if select_fields is not None:
            for field in select_fields:
                if not self.field_exists(field):
                    select_fields.remove(field)

        else:
            select_fields = self.model_fields.keys()

        return {"filters": filters, "ordering": ordering, "select_fields": select_fields}


class RetrieveModelMixin(HandlerMixin):
    """
    Get a model instance and a list of model instances
    """

    def get(self, db: Session, field_name: str, field_value: Any) -> Optional[ModelType]:
        if self.field_exists(field_name) and self.field_is_unique(field_name):
            filters = {field_name: field_value}
            return db.query(self.model).filter_by(**filters).first()

    def list(
        self,
        db: Session,
        skip: int,
        limit: int,
        filters: Optional[dict] = None,
        ordering: Optional[list] = None,
        select_fields: Optional[list] = None,
    ) -> List[ModelType]:

        filters = self.init_get_list_parameters(filters)["filters"]
        ordering = self.init_get_list_parameters(ordering)["ordering"]
        select_fields = self.init_get_list_parameters(select_fields)["select_fields"]

        return (
            db.query(self.model)
            .options(load_only(*select_fields))
            .filter_by(**filters)
            .order_by(*ordering)
            .offset(skip)
            .limit(limit)
            .all()
        )


class CreateModelMixin(Generic[CreateSchemaType]):
    """
    Create a model instance
    """

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        obj = self.model(obj_in_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


class UpdateModelMixin(Generic[UpdateSchemaType]):
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


class DeleteModelMixin:
    """
    Delete a model instance
    """

    def remove(self, db: Session, obj_id: Any) -> ModelType:
        obj = db.query(self.model).get(obj_id)
        db.delete(obj)
        db.commit()
        return obj