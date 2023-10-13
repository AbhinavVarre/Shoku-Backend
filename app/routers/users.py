from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from .. import utils

router = APIRouter(prefix="/users", tags=["users"])


# Create a user
@router.post("/", response_model=schemas.User, summary="Add a user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    db_user = models.Users(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Read all users
@router.get("/", response_model=list[schemas.User], summary="Read all users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.Users).offset(skip).limit(limit).all()
    return users


# Read user by name
@router.get("/{name}", response_model=schemas.User, summary="Read user data by name")
def read_user(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, name=name)
    return db_user


# Read user by id
@router.get(
    "/{user_id}/details", response_model=schemas.User, summary="Read user data by id"
)
def read_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user_id)
    return db_user


# Follow another user
@router.post(
    "/{user}/follow", response_model=schemas.User, summary="Follow another user"
)
def follow_user(
    user: str,
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, name=user)
    current_user.followed.append(user)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


# Unfollow another user
@router.post(
    "/{user}/unfollow", response_model=schemas.User, summary="Unfollow another user"
)
def unfollow_user(
    user: str,
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, name=user)
    if user not in current_user.followed:
        raise HTTPException(status_code=400, detail="User not followed")
    current_user.followed.remove(user)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


# Get followers
@router.get("/followers", response_model=list[schemas.User], summary="Get followers")
def get_followers(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    return current_user.followers.all()


# Get following
@router.get("/following", response_model=list[schemas.User], summary="Get following")
def get_following(
    current_user: models.Users = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    return current_user.followed.all()
