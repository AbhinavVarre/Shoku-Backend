from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from .. import utils


router = APIRouter(
    prefix="/restaurantlist",
    tags=["lists"]
)


#create a list for a user
@router.post("/add", response_model=schemas.RestaurantList, summary="Create a list for a user")
def create_list(list: schemas.RestaurantListCreate, user: models.Users = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    db_restaurant_list = models.RestaurantLists( **list.model_dump(), users=[user])
    db.add(db_restaurant_list)
    db.commit()
    db.refresh(db_restaurant_list)
    return db_restaurant_list

#share list with another user
@router.post("/{list_name}/share/{user_id}", response_model=schemas.RestaurantList, summary="Share list with another user")
def share_list(list_name: str, user_id:int, current_user: models.Users = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    list = read_list(db=db, list_name=list_name, current_user=current_user)
    user = crud.get_user_by_id(db, id=user_id)
    list.users.append(user)
    db.add(list)
    db.commit()
    db.refresh(list)
    return list


#add a restaurant to a user's list
@router.post("/{list_name}/add/{restaurant_name}", response_model=schemas.RestaurantList, summary="Add a restaurant to a user's list")
def add_to_list(list_name: str, restaurant_name:str, current_user: models.Users = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    list = read_list(db=db, list_name=list_name, current_user=current_user)
    restaurant = crud.read_restaurant(db, name=restaurant_name)
    list.restaurants.append(restaurant)
    db.add(list)
    db.commit()
    db.refresh(list)
    return list

#read all lists for a user
@router.get("/all", response_model=list[schemas.RestaurantList],summary="Read all lists for a user")
def read_all_lists(current_user: models.Users = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    return crud.get_user(db, name=current_user.name).lists # type: ignore

#read a user's list
@router.get("read/{list_name}", response_model=schemas.RestaurantList, summary="Read a user's list")
def read_list(list_name: str, current_user: models.Users = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    lists = read_all_lists(db=db, current_user=current_user)
    restaurant_list = next((lst for lst in lists if lst.name == list_name), None)
    if restaurant_list is None:
        raise HTTPException(status_code=404, detail=f"List not found for user {current_user.name}")
    return restaurant_list
