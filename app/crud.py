from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.Users(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_ratings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ratings).offset(skip).limit(limit).all()


def create_user_rating(db: Session, rating: schemas.RatingCreate):
    db_item = models.Ratings(**rating.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
