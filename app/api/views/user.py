from api.dependencies import get_db
from core.auth.exceptions import AccessDeniedException, AuthBaseException
from core.auth.schemas import EmailPasswordRequestForm, RegistrationData, Token, UserOut
from core.auth.utils import authenticate, create_user, generate_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register/", response_model=UserOut)
def register(requested_user: RegistrationData, db: Session = Depends(get_db)):
    try:
        user = create_user(db, requested_user)
    except AuthBaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user


@router.post("/token/", response_model=Token)
def login(form_data: EmailPasswordRequestForm, db: Session = Depends(get_db)):
    try:
        user = authenticate(db, form_data.email, form_data.password)
    except AccessDeniedException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = generate_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
