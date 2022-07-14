from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr, FileUrl, HttpUrl, conint, constr

UUID_LENGTH = 36


class Source(BaseModel):
    id: int
    name: constr(max_length=100)
    link: Union[HttpUrl, None] = None
    description: str
    logo: Union[FileUrl, None] = None

    class Config:
        orm_mode = True


class Theme(BaseModel):
    id: int
    name: constr(max_length=255)
    description: Union[str, None] = None


class News(BaseModel):
    uid: constr(max_length=UUID_LENGTH)
    slug: constr(max_length=255)
    text: str
    uploaded_at: datetime
    original_link: Union[HttpUrl, None] = None
    author: constr(max_length=100) = None
    source: Union[Source, None] = None
    theme: Union[Theme, None] = None


class User(BaseModel):
    uid: constr(max_length=UUID_LENGTH)
    email: EmailStr
    password: str
    image: Union[FileUrl, None] = None


class Rating(BaseModel):
    id: int
    value: conint(gt=0, le=10)
    created_at: datetime
    news: News
    user: User


class Filter(BaseModel):
    id: int
    user: User
    theme: Theme
    applied_at: datetime
