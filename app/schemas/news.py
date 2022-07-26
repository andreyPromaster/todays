from datetime import datetime
from typing import Union

from core.auth.schemas import User
from pydantic import BaseModel, FileUrl, HttpUrl, conint, constr

UUID_LENGTH = 36


class Source(BaseModel):
    id: int
    name: constr(max_length=100)
    link: Union[HttpUrl, None] = None
    description: str
    logo: Union[FileUrl, None] = None

    class Config:
        orm_mode = True


class ThemeBase(BaseModel):
    name: constr(max_length=255)
    description: Union[str, None] = None

    class Config:
        orm_mode = True


class ThemeUpdate(ThemeBase):
    name: Union[constr(max_length=255), None] = None
    description: Union[str, None] = None


class ThemeRetrieve(ThemeBase):
    id: int


class News(BaseModel):
    uid: constr(max_length=UUID_LENGTH)
    slug: constr(max_length=255)
    text: str
    uploaded_at: datetime
    original_link: Union[HttpUrl, None] = None
    author: constr(max_length=100) = None
    source: Union[Source, None] = None
    theme: Union[ThemeRetrieve, None] = None


class Rating(BaseModel):
    id: int
    value: conint(gt=0, le=10)
    created_at: datetime
    news: News
    user: User


class Filter(BaseModel):
    id: int
    user: User
    theme: ThemeRetrieve
    applied_at: datetime
