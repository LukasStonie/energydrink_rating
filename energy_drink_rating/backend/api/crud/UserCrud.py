from sqlalchemy.orm import Session

import backend.api.schemas as schemas
from backend.dataLayer.Models import User


def get_user(db: Session, user_id: int):
    """Fetch a user by their primary key ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """Fetch a user by their unique username (used for Login)."""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    """Create a new user with a pre-hashed password."""
    db_user = User(
        username=user.username,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Fetch a list of users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()
