import factory
from db.models.news import User
from db.models.session import SessionLocal


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_session = SessionLocal()

    email = factory.Sequence(lambda n: f"User-test-{n}@mail.com")
    password = factory.Faker("password")