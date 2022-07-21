from string import punctuation
from typing import List, Union

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, FileUrl, constr, validator

MIN_PASSWORD_LENTH = 8


class Permissions(BaseModel):
    name: str


class User(BaseModel):
    id: int
    email: EmailStr
    password: str
    image: Union[FileUrl, None] = None
    permissions: List[Permissions] = []


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
    password: constr(min_length=MIN_PASSWORD_LENTH)
    second_password: constr(min_length=MIN_PASSWORD_LENTH)

    @validator("second_password")
    def passwords_match(cls, v, values, **kwargs):
        if v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("password")
    def password_must_contain_digit(cls, v, values, **kwargs):
        assert any(map(str.isdigit, v)), "Password must contain digit"
        return v

    @validator("password")
    def password_must_contain_upper(cls, v, values, **kwargs):
        assert any(map(str.isupper, v)), "Password must contain uppercase symbol"
        return v

    @validator("password")
    def password_must_contain_specials(cls, v, values, **kwargs):
        assert any(
            map(lambda item: item in punctuation, v)
        ), "Password must contain uppercase symbol"
        return v


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
