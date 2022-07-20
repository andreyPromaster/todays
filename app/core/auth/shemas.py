from typing import List, Union

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, FileUrl, constr


class Permissions(BaseModel):
    name: str


class User(BaseModel):
    uid: constr(max_length=36)
    email: EmailStr
    password: str
    image: Union[FileUrl, None] = None
    permissions: List[Permissions] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[EmailStr, None] = None


class RegistrationData(BaseModel):
    email: EmailStr
    password: str
    second_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
