from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import backend.api.schemas as schemas
import backend.dataLayer.Models as models
from backend.api.crud import ReviewCrud
from backend.api.dependency import get_db
from backend.api.routers.UserRouter import (
    get_current_user,
)

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=schemas.Review)
def post_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Submit a review. Requires a valid Login token."""
    return ReviewCrud.create_review(db=db, review=review, user_id=current_user.id)


@router.get("/combination/{comb_id}", response_model=list[schemas.Review])
def get_comb_reviews(comb_id: int, db: Session = Depends(get_db)):
    return ReviewCrud.get_reviews_by_combination(db, comb_id=comb_id)
