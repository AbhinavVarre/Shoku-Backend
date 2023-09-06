from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from . import models, schemas, utils
import datetime


# add users
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    db_user = models.Users(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# read all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()


# read user data by name
def get_user(db: Session, name: str) -> models.Users:
    user = db.query(models.Users).filter(models.Users.name == name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# read user data by id
def get_user_by_id(db: Session, id: int) -> models.Users:
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# post a rating from a user for a restaurant
async def create_user_rating(db: Session, rating: schemas.RatingCreate, owner_name: str, picture: UploadFile | None = None):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    owner = get_user(db, name=owner_name)
    pictureUrl = None
    if picture:
        pictureUrl = await utils.upload_file_to_s3(picture)
    db_item = models.Ratings(
        **rating.model_dump(), owner_id=owner.id, created_at=current_date, pictureUrl=pictureUrl
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# read ratings by restaurant
def get_ratings(db: Session, restaurant_id: int):
    return (
        db.query(models.Ratings)
        .filter(models.Ratings.restaurant_id == restaurant_id)
        .all()
    )


# read ratings by user
def read_user_ratings(db: Session, name: str):
    return get_user(db, name=name).ratings


# create a restaurant
def create_restaurant(db: Session, restaurant: schemas.RestaurantCreate):
    db_restaurant = models.Restaurants( **restaurant.model_dump())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


# read all restaurants
def get_restaurants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Restaurants).offset(skip).limit(limit).all()

# read restaurant data by name
def read_restaurant(db: Session, name: str):
    restaurant = (
        db.query(models.Restaurants).filter(models.Restaurants.name == name).first()
    )
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


# read restaurant data by name
def read_restaurant_by_id(db: Session, id: int):
    restaurant = (
        db.query(models.Restaurants).filter(models.Restaurants.id == id).first()
    )
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


# read ratings by restaurant
def read_restaurant_ratings(db: Session, name: str) -> list[models.Ratings]:
    restaurant = read_restaurant(db, name=name)
    return restaurant.ratings

# get average rating for restaurant:
def get_average_rating(db: Session, name: str):
    ratings = read_restaurant_ratings(db, name=name)
    return sum(instance.score for instance in ratings) / len(ratings) if ratings else 0

# create a list for a user
def create_list(db: Session, list: schemas.RestaurantListCreate, owner_name: str):
    user = get_user(db, name=owner_name)
    db_restaurant_list = models.RestaurantLists( **list.model_dump(), owner_id=user.id)
    db.add(db_restaurant_list)
    db.commit()
    db.refresh(db_restaurant_list)
    return db_restaurant_list


# add a restaurant to a user's list
def add_restaurant_to_list(db: Session, owner_name: str, list_name : str, restaurant_name: str):
    list = read_list(db, owner_name=owner_name, name=list_name)
    restaurant = read_restaurant(db, name=restaurant_name)
    list.restaurants.append(restaurant)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return list


# read all lists for a user
def read_lists(db:Session, owner_name: str):
    return get_user(db, name=owner_name).lists


# read a user's list
def read_list(db: Session, owner_name: str, name: str):
    lists = read_lists(db, owner_name=owner_name)
    restaurant_list = next((lst for lst in lists if lst.name == name), None)
    if restaurant_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    return restaurant_list
