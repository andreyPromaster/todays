import uuid
from datetime import datetime

from db.models.utils import get_connection_engine
from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime, Integer, SmallInteger, Text

engine = get_connection_engine()
Base = declarative_base(bind=engine)


class Source(Base):
    __tablename__ = "source"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    link = Column(String(255), nullable=True)
    description = Column(Text(), nullable=False)
    logo = Column(Text(), nullable=True)  # store image link
    news = relationship("News", back_populates="source")


class News(Base):
    __tablename__ = "news"

    uid = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    slug = Column(String(255), nullable=False)
    text = Column(Text(), nullable=False)
    uploaded_at = Column(DateTime(), nullable=False, default=datetime.now)
    original_link = Column(String(255), nullable=True)
    author = Column(String(100), nullable=True)
    source_id = Column(Integer, ForeignKey("source.id"))
    theme_id = Column(Integer, ForeignKey("theme.id"))

    source = relationship("Source", back_populates="news")
    theme = relationship("Theme", back_populates="news")
    ratings = relationship("Rating", back_populates="news")


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True)
    value = Column(SmallInteger(), nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.now)
    news_uid = Column(UUID, ForeignKey("news.uid"), nullable=False)
    user_uid = Column(UUID, ForeignKey("user.uid"), nullable=False)

    news = relationship("News", back_populates="ratings")
    user = relationship("User", back_populates="ratings")


association_premission_table = Table(
    "association_permission",
    Base.metadata,
    Column("user_uid", ForeignKey("user.uid"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    uid = Column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    email = Column(Text(), nullable=False, unique=True)
    password = Column(Text(), nullable=False)
    image = Column(Text(), nullable=True)  # store image link

    permissions = relationship("Permission", secondary=association_premission_table)
    ratings = relationship("Rating", back_populates="user")
    filters = relationship("Filter")


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class Theme(Base):
    __tablename__ = "theme"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text(), nullable=True)
    news = relationship("News", back_populates="theme")


class Filter(Base):
    __tablename__ = "filter"

    id = Column(Integer, primary_key=True)
    theme_id = Column(Integer, ForeignKey("theme.id"), nullable=False)
    user_uid = Column(UUID, ForeignKey("user.uid"), nullable=False)
    applied_at = Column(DateTime(), nullable=False, default=datetime.now)
