import schemas
from backend.api.dependency import (
    get_db,
)
from backend.dataLayer.Models import Drink as DrinkModel
from crud import CombCrud
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/combinations", tags=["Combinations"])


@router.post("/", response_model=schemas.Comb)
def create_new_combination(comb: schemas.CombCreate, db: Session = Depends(get_db)):
    return CombCrud.create_comb(db=db, comb=comb)


@router.get("/", response_model=list[schemas.Comb])
def read_combinations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CombCrud.get_combs(db, skip=skip, limit=limit)


@router.get("/{comb_id}", response_model=schemas.Comb)
def read_combination(comb_id: int, db: Session = Depends(get_db)):
    db_comb = CombCrud.get_comb(db, comb_id=comb_id)
    if db_comb is None:
        raise HTTPException(status_code=404, detail="Comb not found")
    return db_comb


@router.delete("/{comb_id}", response_model=schemas.Comb)
def delete_combination(comb_id: int, db: Session = Depends(get_db)):
    db_comb = CombCrud.delete_comb(db, comb_id=comb_id)
    if db_comb is None:
        raise HTTPException(status_code=404, detail="Comb not found")
    return db_comb


@router.put("/{comb_id}", response_model=schemas.Comb)
def update_combination(comb_id: int, comb: schemas.CombCreate, db: Session = Depends(get_db)):
    db_comb = CombCrud.get_comb(db, comb_id=comb_id)
    if db_comb is None:
        raise HTTPException(status_code=404, detail="Comb not found")

    # Update the name
    db_comb.name = comb.name

    # Update the associated drinks
    ingredients = db.query(DrinkModel).filter(
        DrinkModel.id.in_(comb.drink_ids)).all()
    db_comb.drinks = ingredients

    db.commit()
    db.refresh(db_comb)
    return db_comb
