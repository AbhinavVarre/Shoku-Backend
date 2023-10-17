from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


# Create a restaurant
@router.post("/", response_model=schemas.Restaurant, summary="Create a restaurant")
def create_restaurant(
    restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)
):
    db_restaurant = models.Restaurants(**restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


# delete a restaurant by name  or id
@router.delete(
    "/",
    response_model=schemas.Restaurant,
    summary="Delete a restaurant by name",
)
def delete_restaurant(
    name: Optional[str] = None, id: Optional[UUID] = None, db: Session = Depends(get_db)
):
    if name:
        restaurant = crud.read_restaurant(db, name=name)
    elif id:
        restaurant = crud.read_restaurant_by_id(db, id=id)
    else:
        raise HTTPException(status_code=400, detail="Invalid query parameters")
    db.delete(restaurant)
    db.commit()
    return restaurant


# Read all restaurants
@router.get(
    "/", response_model=list[schemas.Restaurant], summary="Read all restaurants"
)
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurants).offset(skip).limit(limit).all()
    return restaurants


# Combine by-id and by-name into one route and use query parameters to differentiate
@router.get(
    "/search",
    response_model=schemas.Restaurant,
    summary="Search for a restaurant by name or id",
)
def search_restaurant(
    name: Optional[str] = None, id: Optional[UUID] = None, db: Session = Depends(get_db)
):
    if name:
        return crud.read_restaurant(db, name=name)
    elif id:
        return crud.read_restaurant_by_id(db, id=id)
    else:
        raise HTTPException(status_code=400, detail="Invalid query parameters")


# Read ratings by restaurant name
@router.get(
    "/{name}/ratings",
    response_model=list[schemas.Rating],
    summary="Read ratings by restaurant name",
)
def read_restaurant_ratings(name: str, db: Session = Depends(get_db)):
    restaurant = crud.read_restaurant(db, name=name)
    return restaurant.ratings


# Get restaurant average rating
@router.get(
    "/{name}/score", response_model=float, summary="Get restaurant average rating"
)
def read_restaurant_avg_score(name: str, db: Session = Depends(get_db)):
    ratings = crud.read_restaurant(db, name=name).ratings
    # if no ratings so far, return 0
    score = sum(instance.score for instance in ratings) / len(ratings) if ratings else 0
    return score
