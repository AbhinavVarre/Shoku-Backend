from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

#add users
@router.post("/add", response_model=schemas.User, summary="Add a user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

#read all users
@router.get("/", response_model=list[schemas.User], summary="Read all users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

#read user data by name
@router.get("/name/{name}", response_model=schemas.User, summary="Read user data by name")
def read_user(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, name=name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#read user data by id
@router.get("/id/{user_id}", response_model=schemas.User, summary="Read user data by id")
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user