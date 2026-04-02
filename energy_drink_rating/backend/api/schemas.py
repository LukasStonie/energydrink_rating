from typing import List, Optional

from pydantic import BaseModel


class DrinkTypeCreate(BaseModel):
    name: str


class DrinkType(DrinkTypeCreate):
    id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy objects

# --- DRINK SCHEMAS ---


class DrinkCreate(BaseModel):
    name: str
    brand: str
    type_id: int  # Remember the 'type' we discussed earlier


class Drink(DrinkCreate):
    id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy objects

# --- REVIEW SCHEMAS ---


class ReviewCreate(BaseModel):
    rating: int
    comment: Optional[str] = None
    user_id: int
    comb_id: int


class Review(ReviewCreate):
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


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str  # This is the plain text password from the user


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
