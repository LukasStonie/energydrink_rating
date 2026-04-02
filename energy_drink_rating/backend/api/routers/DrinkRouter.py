import schemas
from backend.api.dependency import (
    get_db,
)
from backend.dataLayer.Models import Drink as DrinkModel
from crud import DrinkCrud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/drinks", tags=["Drinks"])


@router.post("/", response_model=schemas.Drink)
def create_new_drink(drink: schemas.DrinkCreate, db: Session = Depends(get_db)):
    return DrinkCrud.create_drink(db=db, drink=drink)


@router.get("/", response_model=list[schemas.Drink])
def read_drinks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return DrinkCrud.get_drinks(db=db, skip=skip, limit=limit)


@router.get("/{drink_id}", response_model=schemas.Drink)
def read_drink(drink_id: int, db: Session = Depends(get_db)):
    db_drink = DrinkCrud.get_drink(db=db, drink_id=drink_id)
    if db_drink is None:
        raise HTTPException(status_code=404, detail="Drink not found")
    return db_drink


@router.delete("/{drink_id}", response_model=schemas.Drink)
def delete_drink(drink_id: int, db: Session = Depends(get_db)):
    db_drink = DrinkCrud.delete_drink(db=db, drink_id=drink_id)
    if db_drink is None:
        raise HTTPException(status_code=404, detail="Drink not found")
    return db_drink


@router.put("/{drink_id}", response_model=schemas.Drink)
def update_drink(drink_id: int, drink: schemas.Drink, db: Session = Depends(get_db)):
    db_drink = DrinkCrud.get_drink(db=db, drink_id=drink_id)
    if db_drink is None:
        raise HTTPException(status_code=404, detail="Drink not found")

    db_drink.name = drink.name
    db_drink.description = drink.description
    db_drink.type_id = drink.type_id

    db.commit()
    db.refresh(db_drink)
    return db_drink
