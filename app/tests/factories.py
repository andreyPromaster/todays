import factory
from db.models.news import Theme, User
from sqlalchemy.orm import Session


def UserFactory(session: Session):
    class _UserFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session_persistence = "commit"
            sqlalchemy_session = session

        email = factory.Sequence(lambda n: f"User-test-{n}@mail.com")
        password = factory.Faker("password")

    return _UserFactory


def ThemeFactory(session: Session):
    class _ThemeFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Theme
            sqlalchemy_session_persistence = "commit"
            sqlalchemy_session = session

        name = factory.Sequence(lambda n: f"Theme-{n}")
        description = "Theme description"

    return _ThemeFactory
