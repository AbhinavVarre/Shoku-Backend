from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)


#post a rating from a user for a restaurant
@router.post("/{owner_name}/new", response_model=schemas.Rating, summary="Post a rating from a user for a restaurant")
def create_rating_for_user(item: schemas.RatingCreate, owner_name: str, db: Session = Depends(get_db)):
    """
    Create a rating for a restaurant, from a specified user.
    """
    return crud.create_user_rating(db=db, rating=item, owner_name=owner_name)

#read ratings by restaurant
@router.get("/{restaurant_id}/read", response_model=list[schemas.Rating], summary="Read ratings by restaurant")
def read_ratings(restaurant_id: int, db: Session = Depends(get_db)):
    items = crud.get_ratings(db, restaurant_id=restaurant_id)
    return items

#read ratings by user
@router.get("/{user_id}/ratings/", response_model=list[schemas.Rating], summary="Read ratings by user")
def read_user_ratings(user_id: int, db: Session = Depends(get_db)):
    """
    Returns the average rating for a restaurant. If there are no raings, returns 0.
    """
    db_user = crud.get_user_by_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.ratings