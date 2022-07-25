from datetime import datetime, timedelta

from api.dependencies import get_db
from core.auth.exceptions import AccessDeniedException, UserAlreadyExistsException
from core.auth.schemas import RegistrationData, TokenData
from core.auth.schemas import User as UserSchema
from core.conf import CoreSettings
from db.models.news import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_context.hash(password)


def generate_access_token(payload: dict) -> str:
    jwt_settings = CoreSettings()
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.TOKEN_ENCRYPTION_ALGORITHM
    )
    return encoded_jwt


def create_user(db: Session, user: RegistrationData) -> User:
    """Replace logic in crud operation"""
    is_email_exists = db.query(db.query(User).filter(User.email == user.email).exists()).scalar()
    if is_email_exists:
        raise UserAlreadyExistsException(f"User with email {user.email} already exists")
    user = User(email=user.email, password=get_password_hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, email: str, password: str) -> User:
    try:
        user = db.query(User).filter(User.email == email).one()
    except (MultipleResultsFound, NoResultFound) as e:
        raise AccessDeniedException from e
    if not verify_password(password, user.password):
        raise AccessDeniedException
    return user


async def login_required(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jwt_settings = CoreSettings()
        payload = jwt.decode(
            token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.TOKEN_ENCRYPTION_ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    try:
        user = db.query(User).filter(User.email == token_data.email).one()
    except (MultipleResultsFound, NoResultFound):
        raise credentials_exception

    return UserSchema(**user)
