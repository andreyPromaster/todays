from db.models.utils import get_connection_engine
from sqlalchemy.orm import sessionmaker

engine = get_connection_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
