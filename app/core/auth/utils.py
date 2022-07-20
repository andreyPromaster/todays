from datetime import datetime, timedelta
from string import punctuation

from core.auth.exceptions import PasswordSecuryException, UserAlreadyExistsException
from core.conf import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
    TOKEN_ENCRYPTION_ALGORITHM,
)
from db.models.news import User
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
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=TOKEN_ENCRYPTION_ALGORITHM)
    return encoded_jwt


def is_password_secury(plain_password: str) -> bool:
    if (
        len(plain_password) >= 8
        and any(map(str.isupper, plain_password))
        and any(map(str.isdigit, plain_password))
        and any(map(lambda item: item in punctuation, plain_password))
    ):
        return True
    return False


def create_user(db: Session, email: EmailStr, password: str):
    """Replace logic in crud operation"""
    is_email_exists = db.query(User).filter(User.email == email).exists()
    if is_email_exists:
        raise UserAlreadyExistsException(f"User with email {email} already exists")
    if is_password_secury(password):
        raise PasswordSecuryException("Password is too easy")
    user = User(email=email, password=get_password_hash(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
