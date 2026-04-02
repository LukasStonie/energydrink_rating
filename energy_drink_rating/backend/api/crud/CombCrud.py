from backend.api import schemas
from backend.dataLayer.Models import Comb as CombModel
from backend.dataLayer.Models import Drink as DrinkModel
from sqlalchemy.orm import Session


def get_comb(db: Session, comb_id: int):
    return db.query(CombModel).filter(CombModel.id == comb_id).first()


def get_combs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CombModel).offset(skip).limit(limit).all()


def create_comb(db: Session, comb: schemas.CombCreate):
    db_comb = CombModel(name=comb.name)
    # Handle the association
    ingredients = db.query(DrinkModel).filter(
        DrinkModel.id.in_(comb.drink_ids)).all()
    db_comb.drinks = ingredients

    db.add(db_comb)
    db.commit()
    db.refresh(db_comb)
    return db_comb


def delete_comb(db: Session, comb_id: int):
    db_obj = db.query(CombModel).get(comb_id)
    db.delete(db_obj)
    db.commit()
    return db_obj
