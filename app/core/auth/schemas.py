from string import punctuation
from typing import List, Union

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, FileUrl, constr, validator

MIN_PASSWORD_LENGTH = 8


class EmailPasswordRequestForm(BaseModel):
    email: EmailStr
    password: str


class Permissions(BaseModel):
    name: str


class User(BaseModel):
    id: int
    email: EmailStr
    image: Union[FileUrl, None] = None
    permissions: List[Permissions] = []

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    image: Union[FileUrl, None] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[EmailStr, None] = None


class RegistrationData(BaseModel):
    email: EmailStr
    password: constr(min_length=MIN_PASSWORD_LENGTH)
    second_password: constr(min_length=MIN_PASSWORD_LENGTH)

    @validator("second_password")
    def passwords_match(cls, value, values, **kwargs):
        if value != values["password"]:
            raise ValueError("Passwords do not match")
        return value

    @validator("password")
    def password_must_contain_digit(cls, password):
        assert any(map(str.isdigit, password)), "Password must contain digit"
        return password

    @validator("password")
    def password_must_contain_upper(cls, password):
        assert any(map(str.isupper, password)), "Password must contain uppercase symbol"
        return password

    @validator("password")
    def password_must_contain_specials(cls, password):
        assert any(
            map(lambda item: item in punctuation, password)
        ), "Password must contain specials symbol"
        return password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
