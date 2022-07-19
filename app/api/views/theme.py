from typing import List

import crud
from api.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas import news as schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{theme_id}", response_model=schemas.ThemeRetrieve)
def get_theme(theme_id: int, db: Session = Depends(get_db)):
    theme = crud.theme.get(db=db, obj_id=theme_id)
    if theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme


@router.get("/", response_model=List[schemas.ThemeRetrieve])
def get_all_themes(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    themes_list = crud.theme.list(db=db, skip=skip, limit=limit)
    return themes_list


@router.post("/", response_model=schemas.ThemeRetrieve)
def create_theme(theme: schemas.ThemeBase, db: Session = Depends(get_db)):
    theme_exists = crud.theme.get_by_name(db=db, name=theme.name)
    if theme_exists:
        raise HTTPException(status_code=400, detail=f"Theme with name {theme.name} already exists")
    theme = crud.theme.create(db=db, obj_in=theme)
    return theme


@router.put("/{theme_id}", response_model=schemas.ThemeRetrieve)
def update_theme(update_data: schemas.ThemeUpdate, theme_id: int, db: Session = Depends(get_db)):
    theme = crud.theme.get(db=db, obj_id=theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    updated_theme = crud.theme.update(db=db, update_data=update_data, obj_db=theme)
    return updated_theme


@router.delete("/{theme_id}", response_model=schemas.ThemeRetrieve)
def delete_theme(theme_id: int, db: Session = Depends(get_db)):
    theme = crud.theme.get(db=db, obj_id=theme_id)
    if not theme:
        raise HTTPException(status_code=404, detail="Theme not found")

    return crud.theme.remove(db=db, obj_id=theme_id)
