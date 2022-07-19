from typing import Generic, Type, TypeVar

from db.models.news import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        * `model`: A SQLAlchemy model class
        """
        self.model = model
