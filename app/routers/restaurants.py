from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"]
)


#create a restaurant
@router.post("/add", response_model=schemas.Restaurant, summary="Create a restaurant")
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.create_restaurant(db=db, restaurant=restaurant)

#read all restaurants
@router.get("/", response_model=list[schemas.Restaurant], summary="Read all restaurants")
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_restaurants(db, skip=skip, limit=limit)
    return users

#read restaurant data by name
@router.get("/name/{name}", response_model=schemas.Restaurant, summary="Read restaurant data by name")
def read_restaurant(name: str, db: Session = Depends(get_db)):
    db_restaurant = crud.read_restaurant(db, name=name)
    return db_restaurant

#read restaurant data by id
@router.get("/id/{name}", response_model=schemas.Restaurant, summary="Read restaurant data by id")
def read_restaurant_by_id(id: int, db: Session = Depends(get_db)):
    db_restaurant = crud.read_restaurant_by_id(db, id=id)
    return db_restaurant

#read ratings by restaurant name
@router.get("/ratings/name/{name}", response_model=list[schemas.Rating], summary="Read ratings by restaurant name")
def read_restaurant_ratings(name: str, db: Session = Depends(get_db)):
    ratings = crud.read_restaurant_ratings(db, name=name)
    return ratings


#get restaurant average rating
@router.get("/{name}/score", response_model=float, summary="Get restaurant average rating")
def read_restaurant_avg_score(name: str, db: Session = Depends(get_db)):
    score = crud.get_average_rating(db, name=name)
    return score