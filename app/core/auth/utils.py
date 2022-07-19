from datetime import timedelta, utcnow

from core.conf import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    TOKEN_ENCRYPTION_ALGORITHM,
)
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.orm import Session

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def generate_access_token(payload: dict) -> str:
    to_encode = payload.copy()
    expire = utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=TOKEN_ENCRYPTION_ALGORITHM)
    return encoded_jwt


def create_user(db: Session, email: EmailStr, password: str):
    #  check if user email already exists, hash password,
    #  check if password is too easy
    pass
