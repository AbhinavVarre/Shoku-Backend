from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models

from .. import crud, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


