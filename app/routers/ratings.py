from fastapi import Depends, FastAPI, HTTPException, APIRouter, UploadFile, File, Form
from app import schemas, models, crud, oauth2, utils
from app.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated, Tuple
from pydantic import ValidationError
import json
from uuid import UUID

router = APIRouter(prefix="/ratings", tags=["ratings"])


# post a rating from a user for a restaurant
@router.post(
    "/new",
    response_model=schemas.Rating,
    summary="Post a rating from a user for a restaurant",
)
async def create_rating_for_user(
    item_json: str = Form(...),  # Expect the data as a stringified JSON,
    db: Session = Depends(get_db),
    owner: models.Users = Depends(oauth2.get_current_user),
    picture: UploadFile = File(None),
):
    """
    input a json containing the following fields: score, restaurant, and optionally a review like {\"score\": 0, \"restaurant_name\": \"kims\", \"review\": \"pretty good\"}
    """
    try:
        # Convert the stringified JSON to a dict
        item_data = json.loads(item_json)
        # Convert the dict to the desired Pydantic model
        item = schemas.RatingCreate(**item_data)
    except (json.JSONDecodeError, ValidationError):
        raise HTTPException(status_code=400, detail="Invalid item data")

    db_item = models.Ratings(
        **item.model_dump(exclude={"restaurant_name"}),
        owner_id=owner.id,
        restaurant_id=crud.read_restaurant(db, name=item.restaurant_name).id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    if picture:
        rating_id = db_item.id
        db_picture = await utils.create_picture(
            picture=picture,
            rating_id=rating_id,  # type: ignore
            owner_id=owner.id,  # type: ignore
            db=db,
        )
        db_item.pictures.append(db_picture)
        db.commit()
        db.refresh(db_item)
    return db_item


# read ratings by restaurant
@router.get(
    "/{restaurant}/read",
    response_model=list[schemas.Rating],
    summary="Read ratings by restaurant",
)
def read_ratings(restaurant: str, db: Session = Depends(get_db)):
    items = crud.get_ratings(db, restaurant=restaurant)
    return items


# read ratings by user
@router.get(
    "/{user}/ratings/",
    response_model=list[schemas.Rating],
    summary="Read ratings by user",
)
def read_user_ratings(user: str, db: Session = Depends(get_db)):
    """
    Returns the average rating for a restaurant. If there are no raings, returns 0.
    """
    db_user = crud.get_user(db, name=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.ratings
