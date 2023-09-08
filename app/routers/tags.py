from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from app.database import get_db
from sqlalchemy.orm import Session
from .. import utils


router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


#Create a tag
@router.post("/add", response_model=schemas.Tag, summary="create a tag")
def create_tag(tag: schemas.Tag, db: Session = Depends(get_db)):
    pass

#Tag a restaurant
@router.post("/{restaurant_name}/add/{tag_name}", response_model=schemas.Restaurant, summary="Tag a restaurant")
def tag_restaurant(restaurant_name: str, tag_name, db: Session = Depends(get_db)):
    pass

#Read all restaurants assocaited with a tag
@router.get("/{tag_name}/restaurants", response_model=list[schemas.Restaurant],summary="Read all restaurants assocaited with a tag")
def get_restaurants_by_tag(tag_name: str, db: Session = Depends(get_db)):
    pass

#Read all tags associated with a restaurant
@router.get("/{restaurant_name}/tags", response_model=list[schemas.Tag], summary="Read all tags associated with a restaurant")
def get_tags_by_restaurant(restaurant_name: str, db: Session = Depends(get_db)):
    pass