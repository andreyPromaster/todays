from typing import List

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

    def filter_by_partial_name(self, db: Session, name: str) -> List[ModelType]:
        queryset = db.query(self.model).filter(self.model.name.contains(name)).all()
        return queryset


theme = CRUDTheme(Theme)
