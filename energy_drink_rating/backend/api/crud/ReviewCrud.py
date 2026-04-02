from sqlalchemy.orm import Session

import backend.api.schemas as schemas
from backend.dataLayer.Models import Review


def create_review(db: Session, review: schemas.ReviewCreate, user_id: int):
    """
    Create a new review. 
    Note: user_id comes from the Auth token, not the request body!
    """
    db_review = Review(
        rating=review.rating,
        comment=review.comment,
        comb_id=review.comb_id,
        user_id=user_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()


def update_review(db: Session, review_id: int, review_update: schemas.ReviewCreate):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        return None
    if review_update.rating is not None:
        db_review.rating = review_update.rating
    if review_update.comment is not None:
        db_review.comment = review_update.comment
    db.commit()
    db.refresh(db_review)
    return db_review


def delete_review(db: Session, review_id: int):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        return None
    db.delete(db_review)
    db.commit()
    return db_review


def get_reviews_by_combination(db: Session, comb_id: int):
    return db.query(Review).filter(Review.comb_id == comb_id).all()
