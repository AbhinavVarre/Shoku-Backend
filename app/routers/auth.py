from fastapi import Depends, HTTPException, APIRouter, status
from app import schemas, models, crud, utils, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["authentication"]
)


@router.post("/login", response_model=schemas.Token, summary="Login function")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.name == user_credentials.username).first()

    # no such username
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # wrong password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create and return token
    # can add fields to payload if needed, upadate schemas.TokenData accordingly
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}