from fastapi import Depends, FastAPI, HTTPException, APIRouter, UploadFile, File, Form
from app import schemas, models, crud, oauth2, utils
from app.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated, Tuple
from pydantic import ValidationError
import json

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"]
)


#post a rating from a user for a restaurant
@router.post("/new", response_model=schemas.Rating, summary="Post a rating from a user for a restaurant", description="input a json containing the following fields: score, restaurant_id, and optionally a review")
def create_rating_for_user(
    item_json: str = Form(...),  # Expect the data as a stringified JSON,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
    picture: UploadFile = File(None) 
):
    try:
        # Convert the stringified JSON to a dict
        item_data = json.loads(item_json)
        # Convert the dict to the desired Pydantic model
        item = schemas.RatingCreate(**item_data)
    except (json.JSONDecodeError, ValidationError):
        raise HTTPException(status_code=400, detail="Invalid item data")
    
    return crud.create_user_rating(db=db, rating=item, owner_name=current_user, picture=picture)

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