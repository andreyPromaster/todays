from string import punctuation
from typing import List, Union

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, FileUrl, constr, validator


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

    @validator("password", pre=True)
    def passwords_match(cls, v, values, **kwargs):
        if "second_password" in values and v != values["second_password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("password")
    def password_lenth(cls, v, values, **kwargs):
        PASSWORD_LENTH = 8
        assert len(v) >= PASSWORD_LENTH, f"Password must be longer than {PASSWORD_LENTH} symbols"

    @validator("password")
    def password_must_contain_digit(cls, v, values, **kwargs):
        assert any(map(str.isdigit, v)), "Password must contain digit"

    @validator("password")
    def password_must_contain_upper(cls, v, values, **kwargs):
        assert any(map(str.isupper, v)), "Password must contain uppercase symbol"

    @validator("password")
    def password_must_contain_specials(cls, v, values, **kwargs):
        assert any(
            map(lambda item: item in punctuation, v)
        ), "Password must contain uppercase symbol"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
