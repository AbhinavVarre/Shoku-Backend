from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/restaurantlist",
    tags=["lists"]
)


#create a list for a user
@router.post("/{owner_name}/add", response_model=schemas.RestaurantList, summary="Create a list for a user")
def create_list(list: schemas.RestaurantListCreate, owner_name: str, db: Session = Depends(get_db)):
    return crud.create_list(db=db, list=list, owner_name=owner_name)

#add a restaurant to a user's list
@router.post("/{owner_name}/{list_name}/add/{restaurant_name}", response_model=schemas.RestaurantList, tags=["lists"], summary="Add a restaurant to a user's list")
def add_to_list(owner_name: str, list_name: str, restaurant_name:str, db: Session = Depends(get_db)):
    return crud.add_restaurant_to_list(db=db, owner_name=owner_name, list_name = list_name, restaurant_name=restaurant_name)

#read all lists for a user
@router.get("/{owner_name}/all", response_model=list[schemas.RestaurantList],summary="Read all lists for a user")
def read_all_lists(owner_name: str, db: Session = Depends(get_db)):
    return crud.read_lists(db=db, owner_name=owner_name)

#read a user's list
@router.get("/{owner_name}/{list_name}", response_model=schemas.RestaurantList, summary="Read a user's list")
def read_list(owner_name: str, list_name: str, db: Session = Depends(get_db)):
    return crud.read_list(db=db, owner_name=owner_name, name=list_name)
