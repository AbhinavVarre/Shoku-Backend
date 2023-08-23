from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
import datetime


#add users
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.Users(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#read all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()

#read user data by name
def get_user(db: Session, name: str) -> models.Users:
    return db.query(models.Users).filter(models.Users.name == name).first()

#read user data by id
def get_user_by_id(db: Session, id: int) -> models.Users:
    return db.query(models.Users).filter(models.Users.id == id).first()

#post a rating from a user for a restaurant
def create_user_rating(db: Session, rating: schemas.RatingCreate, owner_name : str):
    current_date = datetime.datetime.now()
    owner = get_user(db, name=owner_name)
    if owner is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_item = models.Ratings(**rating.model_dump(), owner_id=owner.id, date=current_date)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#read ratings by restaurant
def get_ratings(db: Session, restaurant_id: int):
    return db.query(models.Ratings).filter(models.Ratings.restaurant_id == restaurant_id).all()


#read ratings by user
def read_user_ratings(db: Session, owner_id: int, name: str):
    return get_user(db, name=name).ratings

#create a restaurant
def create_restaurant():
    pass

#read restaurant data by name
def read_restaurant():
    pass

#read ratings by restaurant
def read_restaurant_ratings():
    pass

#create a list for a user
def create_list():
    pass

#add a restaurant to a user's list
def add_restaurant_to_list():
    pass

#remove a restaurant from a user's list
def remove_restaurant_from_list():
    pass

#read all lists for a user
def read_lists():
    pass

#read a user's list
def read_list():
    pass

