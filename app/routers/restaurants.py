from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"]
)


#create a restaurant
@router.post("/add", response_model=schemas.Restaurant, summary="Create a restaurant")
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = models.Restaurants( **restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

#read all restaurants
@router.get("/", response_model=list[schemas.Restaurant], summary="Read all restaurants")
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurants).offset(skip).limit(limit).all()
    return restaurants

#read restaurant data by name
@router.get("/name/{name}", response_model=schemas.Restaurant, summary="Read restaurant data by name")
def read_restaurant(name: str, db: Session = Depends(get_db)):
    db_restaurant = crud.read_restaurant(db, name=name)
    return db_restaurant

#read restaurant data by id
@router.get("/id/{id}", response_model=schemas.Restaurant, summary="Read restaurant data by id")
def read_restaurant_by_id(id: UUID, db: Session = Depends(get_db)):

    db_restaurant = crud.read_restaurant_by_id(db, id=id)
    return db_restaurant

#read ratings by restaurant name
@router.get("/ratings/name/{name}", response_model=list[schemas.Rating], summary="Read ratings by restaurant name")
def read_restaurant_ratings(name: str, db: Session = Depends(get_db)):
    restaurant = crud.read_restaurant(db, name=name)
    return restaurant.ratings


#get restaurant average rating
@router.get("/{name}/score", response_model=float, summary="Get restaurant average rating")
def read_restaurant_avg_score(name: str, db: Session = Depends(get_db)):
    ratings = crud.read_restaurant(db, name=name).ratings
    # if no ratings so far, return 0
    score =  sum(instance.score for instance in ratings) / len(ratings) if ratings else 0
    return score