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
@router.post("/{owner_name}/add", response_model=schemas.RestaurantList, summary="create a tag")
def create_tag(list: schemas.RestaurantListCreate, owner_name: str, db: Session = Depends(get_db)):
    pass

#Tag a restaurant
@router.post("/{owner_name}/{list_name}/add/{restaurant_name}", response_model=schemas.RestaurantList, summary="Tag a restaurant")
def tag_restaurant(owner_name: str, list_name: str, restaurant_name:str, db: Session = Depends(get_db)):
    pass

#Read all restaurants assocaited with a tag
@router.get("/{owner_name}/all", response_model=list[schemas.Restaurant],summary="Read all restaurants assocaited with a tag")
def get_restaurants_by_tag(owner_name: str, db: Session = Depends(get_db)):
    pass

#Read all tags associated with a restaurant
@router.get("/{owner_name}/{list_name}", response_model=list[schemas.Tag], summary="Read all tags associated with a restaurant")
def get_tags_by_restaurant(owner_name: str, list_name: str, db: Session = Depends(get_db)):
    pass