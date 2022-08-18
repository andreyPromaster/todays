import factory
from db.models.news import News, Theme, User
from tests.utils import TestingSessionLocal


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = TestingSessionLocal()

    email = factory.Sequence(lambda n: f"User-test-{n}@mail.com")
    password = factory.Faker("password")


class ThemeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Theme
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = TestingSessionLocal()

    name = factory.Sequence(lambda n: f"theme#{n:03}")
    description = "description for theme"


class NewsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = News
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = TestingSessionLocal()

    theme = factory.SubFactory(ThemeFactory)
