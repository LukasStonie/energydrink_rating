from backend.api import schemas
from backend.dataLayer.Models import DrinkType as DrinkTypeModel
from sqlalchemy.orm import Session


def get_drink_type(db: Session, drink_type_id: int):
    return db.query(DrinkTypeModel).filter(DrinkTypeModel.id == drink_type_id).first()


def get_drink_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DrinkTypeModel).offset(skip).limit(limit).all()


def create_drink_type(db: Session, drink_type: schemas.DrinkTypeCreate):
    db_drink_type = DrinkTypeModel(name=drink_type.name)
    db.add(db_drink_type)
    db.commit()
    db.refresh(db_drink_type)
    return db_drink_type


def delete_drink_type(db: Session, drink_type_id: int):
    db_obj = db.get(DrinkTypeModel, drink_type_id)
    if db_obj is None:
        return None
    db.delete(db_obj)
    db.commit()
    return db_obj
