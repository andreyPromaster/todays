from typing import List

from api.dependencies import get_db
from db.models import news as models
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import news as schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{theme_id}", response_model=schemas.ThemeRetrieve)
def get_theme(theme_id: int, db: Session = Depends(get_db)):
    theme = db.query(models.Theme).filter(models.Theme.id == theme_id).first()
    if theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme


@router.get("/", response_model=List[schemas.ThemeRetrieve])
def get_all_themes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return db.query(models.Theme).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.ThemeRetrieve)
def create_theme(theme: schemas.ThemeBase, db: Session = Depends(get_db)):
    theme = models.Theme(name=theme.name, description=theme.description)
    theme_exists = db.query(models.Theme).filter(models.Theme.name == theme.name).first()
    if theme_exists:
        raise HTTPException(status_code=400, detail=f"Theme {theme.name} already exists")
    db.add(theme)
    db.commit()
    db.refresh(theme)
    return theme


@router.put("/{theme_id}", response_model=schemas.ThemeRetrieve)
def update_theme(update_data: schemas.ThemeUpdate, theme_id: int, db: Session = Depends(get_db)):
    theme = db.query(models.Theme).filter(models.Theme.id == theme_id).first()
    update_data = jsonable_encoder(update_data)

    for field in update_data:
        if update_data.get(field):
            setattr(theme, field, update_data[field])

    db.add(theme)
    db.commit()
    db.refresh(theme)
    return theme


@router.delete("/{theme_id}", response_model=schemas.ThemeRetrieve)
def delete_theme(theme_id: int, db: Session = Depends(get_db)):
    theme = db.query(models.Theme).get(theme_id)
    if theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")

    db.delete(theme)
    db.commit()
    return theme
