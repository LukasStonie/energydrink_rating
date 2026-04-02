from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import backend.api.schemas as schemas
from backend.api.crud import DrinkTypeCrud
from backend.api.dependency import (
    get_db,
)

router = APIRouter(prefix="/drink-types", tags=["Drink Types"])


@router.post("/", response_model=schemas.DrinkType)
def create_new_drink_type(drink_type: schemas.DrinkTypeCreate, db: Session = Depends(get_db)):
    return DrinkTypeCrud.create_drink_type(db=db, drink_type=drink_type)


@router.get("/", response_model=list[schemas.DrinkType])
def read_drink_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return DrinkTypeCrud.get_drink_types(db=db, skip=skip, limit=limit)


@router.get("/{drink_type_id}", response_model=schemas.DrinkType)
def read_drink_type(drink_type_id: int, db: Session = Depends(get_db)):
    db_drink_type = DrinkTypeCrud.get_drink_type(
        db=db, drink_type_id=drink_type_id)
    if db_drink_type is None:
        raise HTTPException(status_code=404, detail="Drink type not found")
    return db_drink_type


@router.delete("/{drink_type_id}", response_model=schemas.DrinkType)
def delete_drink_type(drink_type_id: int, db: Session = Depends(get_db)):
    db_drink_type = DrinkTypeCrud.delete_drink_type(
        db=db, drink_type_id=drink_type_id)
    if db_drink_type is None:
        raise HTTPException(status_code=404, detail="Drink type not found")
    return db_drink_type


@router.put("/{drink_type_id}", response_model=schemas.DrinkType)
def update_drink_type(drink_type_id: int, drink_type: schemas.DrinkType, db: Session = Depends(get_db)):
    db_drink_type = DrinkTypeCrud.get_drink_type(
        db=db, drink_type_id=drink_type_id)
    if db_drink_type is None:
        raise HTTPException(status_code=404, detail="Drink type not found")

    db_drink_type.name = drink_type.name

    db.commit()
    db.refresh(db_drink_type)
    return db_drink_type
