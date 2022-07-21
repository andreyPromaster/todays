from api.dependencies import get_db
from core.auth.shemas import RegistrationData
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register")
def register(user: RegistrationData, db: Session = Depends(get_db)):
    pass
