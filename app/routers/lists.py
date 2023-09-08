from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from app.database import get_db
from sqlalchemy.orm import Session
from .. import utils


router = APIRouter(
    prefix="/restaurantlist",
    tags=["lists"]
)


#create a list for a user
@router.post("/{owner_name}/add", response_model=schemas.RestaurantList, summary="Create a list for a user")
def create_list(list: schemas.RestaurantListCreate, owner_name: str, db: Session = Depends(get_db)):
    user =crud.get_user(db, name=owner_name)
    db_restaurant_list = models.RestaurantLists( **list.model_dump(), owner_id=user.id)
    db.add(db_restaurant_list)
    db.commit()
    db.refresh(db_restaurant_list)
    return db_restaurant_list

#add a restaurant to a user's list
@router.post("/{owner_name}/{list_name}/add/{restaurant_name}", response_model=schemas.RestaurantList, summary="Add a restaurant to a user's list")
def add_to_list(owner_name: str, list_name: str, restaurant_name:str, db: Session = Depends(get_db)):
    list = read_list(owner_name=owner_name, list_name=list_name)
    restaurant = crud.read_restaurant(db, name=restaurant_name)
    list.restaurants.append(restaurant)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return list

#read all lists for a user
@router.get("/{owner_name}/all", response_model=list[schemas.RestaurantList],summary="Read all lists for a user")
def read_all_lists(owner_name: str, db: Session = Depends(get_db)):
    return crud.get_user(db, name=owner_name).lists

#read a user's list
@router.get("/{owner_name}/{list_name}", response_model=schemas.RestaurantList, summary="Read a user's list")
def read_list(owner_name: str, list_name: str, db: Session = Depends(get_db)):
    lists = read_all_lists(owner_name=owner_name)
    restaurant_list = next((lst for lst in lists if lst.name == owner_name), None)
    if restaurant_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    return restaurant_list
