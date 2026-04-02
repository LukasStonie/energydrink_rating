from typing import List, Optional

from pydantic import BaseModel


# --- DRINK SCHEMAS ---
class DrinkBase(BaseModel):
    brand: str
    flavor: str


class Drink(DrinkBase):
    id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy objects

# --- REVIEW SCHEMAS ---


class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    user_id: int
    comb_id: int


class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True

# --- COMBINATION SCHEMAS ---


class CombBase(BaseModel):
    name: str


class CombCreate(CombBase):
    drink_ids: List[int]  # Used when creating a new mix


class Comb(CombBase):
    id: int
    drinks: List[Drink] = []
    reviews: List[Review] = []

    class Config:
        from_attributes = True
