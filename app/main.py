from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "ratings",
        "description": "Add  and read ratings",
    },
    {
        "name": "restaurants",
        "description": "Create and manage restaurants",
    },
    {
        "name": "lists",
        "description": "Create, upload to, and delete from lists.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

#add users
@app.post("/users/add", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

#read all users
@app.get("/users/", response_model=list[schemas.User], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#read user data by name
@app.get("/users/name/{name}", response_model=schemas.User, tags=["users"])
def read_user(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, name=name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#read user data by id
@app.get("/users/id/{user_id}", response_model=schemas.User, tags=["users"])
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#post a rating from a user for a restaurant
@app.post("/users/{owner_name}/ratings/new", response_model=schemas.Rating, tags=["ratings"])
def create_rating_for_user(item: schemas.RatingCreate, owner_name: str, db: Session = Depends(get_db)):
    return crud.create_user_rating(db=db, rating=item, owner_name=owner_name)

#read ratings by restaurant
@app.get("/restaurant/{restaurant_id}/ratings/", response_model=list[schemas.Rating], tags=["ratings"])
def read_ratings(restaurant_id: int, db: Session = Depends(get_db)):
    items = crud.get_ratings(db, restaurant_id=restaurant_id)
    return items

#read ratings by user
@app.get("/users/{user_id}/ratings/", response_model=list[schemas.Rating], tags=["ratings"])
def read_user_ratings(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.ratings

#create a restaurant
@app.post("/restaurants/add", response_model=schemas.Restaurant, tags=["restaurants"])
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    return crud.create_restaurant(db=db, restaurant=restaurant)

#read all restaurants
@app.get("/restaurants/", response_model=list[schemas.Restaurant], tags=["restaurants"])
def read_restaurants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_restaurants(db, skip=skip, limit=limit)
    return users

#read restaurant data by name
@app.get("/restaurants/name/{name}", response_model=schemas.Restaurant, tags=["restaurants"])
def read_restaurant(name: str, db: Session = Depends(get_db)):
    db_restaurant = crud.read_restaurant(db, name=name)
    return db_restaurant

#read restaurant data by id
@app.get("/restaurants/id/{name}", response_model=schemas.Restaurant, tags=["restaurants"])
def read_restaurant_by_id(id: int, db: Session = Depends(get_db)):
    db_restaurant = crud.read_restaurant_by_id(db, id=id)
    return db_restaurant

#read ratings by restaurant name
@app.get("/restaurants/ratings/name/{name}", response_model=list[schemas.Rating], tags=["ratings"])
def read_restaurant_ratings(name: str, db: Session = Depends(get_db)):
    ratings = crud.read_restaurant_ratings(db, name=name)
    return ratings


#get restaurant average rating
@app.get("/restaurants/{name}/score", response_model=float, tags=["restaurants"])
def read_restaurant_avg_score(name: str, db: Session = Depends(get_db)):
    score = crud.get_average_rating(db, name=name)
    return score

#create a list for a user
@app.post("/restaurantlist/{owner_name}/add", response_model=schemas.RestaurantList, tags=["lists"])
def create_list(list: schemas.RestaurantListCreate, owner_name: str, db: Session = Depends(get_db)):
    return crud.create_list(db=db, list=list, owner_name=owner_name)

#add a restaurant to a user's list
@app.post("/restaurantlist/{owner_name}/{list_name}/add/{restaurant_name}", response_model=schemas.RestaurantList, tags=["lists"])
def add_to_list(owner_name: str, list_name: str, restaurant_name:str, db: Session = Depends(get_db)):
    return crud.add_restaurant_to_list(db=db, owner_name=owner_name, list_name = list_name, restaurant_name=restaurant_name)

#read all lists for a user
@app.get("/restaurantlist/{owner_name}/all", response_model=list[schemas.RestaurantList], tags=["lists"])
def read_all_lists(owner_name: str, db: Session = Depends(get_db)):
    return crud.read_lists(db=db, owner_name=owner_name)

#read a user's list
@app.get("/restaurantlist/{owner_name}/{list_name}", response_model=schemas.RestaurantList, tags=["lists"])
def read_list(owner_name: str, list_name: str, db: Session = Depends(get_db)):
    return crud.read_list(db=db, owner_name=owner_name, name=list_name)
