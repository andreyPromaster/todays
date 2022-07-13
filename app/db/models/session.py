from sqlalchemy.orm import sessionmaker

from app.db.models.utils import get_connection_engine

engine = get_connection_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
