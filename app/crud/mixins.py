from typing import Any, Generic, List, Optional, Tuple, TypeVar

from crud.base import ModelType
from crud.exceptions import WrongModelFieldException
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

    def is_field_exists(self, field_name: str):
        if field_name not in self.model_fields.keys():
            raise WrongModelFieldException(
                f"field <{field_name}> doesn't exist for model {self.model}"
            )

    def is_field_unique(self, field_name: str):
        if not (
            self.model_fields.get(field_name).primary_key
            or self.model_fields.get(field_name).unique
        ):
            raise WrongModelFieldException(f"field <{field_name}> is not unique for {self.model}")

    def init_list_parameters(
        self,
        filters: Optional[dict] = None,
        ordering: Optional[list] = None,
        select_fields: Optional[list] = None,
    ) -> Tuple:

        if filters is None:
            filters = {}

        if ordering is None:
            ordering = []

        if select_fields is None:
            select_fields = self.model_fields.keys()

        return filters, ordering, select_fields


class RetrieveModelMixin(HandlerMixin):
    """
    Get a model instance and a list of model instances
    """

    def get(self, db: Session, field_name: str, field_value: Any) -> Optional[ModelType]:
        self.is_field_exists(field_name)
        self.is_field_unique(field_name)
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

        filters, ordering, select_fields = self.init_list_parameters(
            filters, ordering, select_fields
        )

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
