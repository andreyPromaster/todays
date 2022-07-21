from api.dependencies import get_db
from core.auth.exceptions import AuthBaseException
from core.auth.shemas import RegistrationData, UserOut
from core.auth.utils import create_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register/", response_model=UserOut)
def register(requested_user: RegistrationData, db: Session = Depends(get_db)):
    try:
        user = create_user(db, requested_user)
    except AuthBaseException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user
