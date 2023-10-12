from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from . import models, schemas, utils, crud
import datetime
from uuid import UUID


# read user data by name
def get_user(db: Session, name: str) -> models.Users:
    user = db.query(models.Users).filter(models.Users.name == name).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# read user data by id
def get_user_by_id(db: Session, id: UUID) -> models.Users:
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# read ratings by restaurant
def get_ratings(db: Session, restaurant: str):
    restaurant = crud.read_restaurant(db, name=restaurant)
    ratings = (
        db.query(models.Ratings)
        .filter(models.Ratings.restaurant_id == restaurant.id)
        .all()
    )
    return ratings


# read restaurant data by name
def read_restaurant(db: Session, name: str):
    restaurant = (
        db.query(models.Restaurants).filter(models.Restaurants.name == name).first()
    )
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


# read restaurant data by id
def read_restaurant_by_id(db: Session, id: UUID):
    restaurant = (
        db.query(models.Restaurants).filter(models.Restaurants.id == id).first()
    )
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
