from backend.api import schemas
from backend.dataLayer.Models import Drink as DrinkModel
from sqlalchemy.orm import Session


def get_drink(db: Session, drink_id: int):
    return db.query(DrinkModel).filter(DrinkModel.id == drink_id).first()


def get_drinks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DrinkModel).offset(skip).limit(limit).all()


def create_drink(db: Session, drink: schemas.Drink):
    db_drink = DrinkModel(name=drink.name, brand=drink.brand,
                          type_id=drink.type_id)
    db.add(db_drink)
    db.commit()
    db.refresh(db_drink)
    return db_drink


def delete_drink(db: Session, drink_id: int):
    db_obj = db.get(DrinkModel, drink_id)
    if db_obj is None:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj
