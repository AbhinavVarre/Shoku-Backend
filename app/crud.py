from sqlalchemy.orm import Session

from . import models, schemas

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
def get_user(db: Session, name: int):
    return db.query(models.Users).filter(models.Users.name == name).first()

#post a rating from a user for a restaurant
def create_user_rating(db: Session, rating: schemas.RatingCreate):
    db_item = models.Ratings(**rating.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#read ratings by restaurant
def get_ratings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ratings).offset(skip).limit(limit).all()


#read ratings by user
def read_user_ratings():
    pass

#create a restaurant


#read restaurant data by name

#read ratings by restaurant

#create a list for a user

#add a restaurant to a user's list

#remove a restaurant from a user's list

#read all lists for a user

#read a user's list

