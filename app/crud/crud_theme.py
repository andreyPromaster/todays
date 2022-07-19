from typing import List

from cfgv import Optional
from crud import mixins
from crud.base import CRUDBase, ModelType
from db.models.news import Theme
from sqlalchemy.orm import Session


class CRUDTheme(
    CRUDBase[Theme],
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DeleteModelMixin,
):
    """
    all methods for work with db with model Theme
    """

    def get_by_name(self, db: Session, name: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.name == name).first()

    def filter_by_name(self, db: Session, name: str) -> List[ModelType]:
        queryset = db.query(self.model).all()
        filtered = []
        for obj in queryset:
            if name.lower in obj.name.lower:
                filtered.append(obj)
        return filtered


theme = CRUDTheme(Theme)
