from fastapi import Depends, FastAPI, HTTPException, APIRouter, UploadFile, File, Form
from app import schemas, models, crud, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from .. import utils
from uuid import UUID
import json
from pydantic import ValidationError


router = APIRouter(
    prefix="/restaurantlist",
    tags=["lists"]
)


#create a list for a user
@router.post("/lists", response_model=schemas.RestaurantList, summary="Create a list for a user")
async def create_list(
    list_json: str = Form(...),  # Expect the data as a stringified JSON, 
    user: models.Users = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db), 
    picture: UploadFile = File(None)
):
    """
    input a json containing the following fields: name, and description {\"name\": \"places\", \"description\": \"fire places\"}
    """
    try:
        # Convert the stringified JSON to a dict
        list_data = json.loads(list_json)
        # Convert the dict to the desired Pydantic model
        list = schemas.RestaurantListCreate(**list_data)
    except (json.JSONDecodeError, ValidationError):
        raise HTTPException(status_code=400, detail="Invalid item data")
    
    db_restaurant_list = models.RestaurantLists(**list.model_dump(), users=[user])
    db.add(db_restaurant_list)

    if picture:
        db_picture = await utils.create_picture(
            picture=picture,
            owner_id=user.id,  # type: ignore
            db=db,
        )
        db_restaurant_list.cover_picture = db_picture

    db.commit()
    db.refresh(db_restaurant_list)
    return db_restaurant_list

#share list with another user
@router.post("/{list_name}/share/{user}", response_model=schemas.RestaurantList, summary="Share list with another user")
def share_list(list_name: str, user:str, current_user: models.Users = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    list = read_list(db=db, list_name=list_name, current_user=current_user)
    user = crud.get_user(db, name=user)
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
@router.get("/read/{list_name}", response_model=schemas.RestaurantList, summary="Read a user's list")
def read_list(list_name: str, current_user: models.Users = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    lists = read_all_lists(db=db, current_user=current_user)
    restaurant_list = next((lst for lst in lists if lst.name == list_name), None)
    if restaurant_list is None:
        raise HTTPException(status_code=404, detail=f"List not found for user {current_user.name}")
    return restaurant_list

#create/update list cover photo
@router.post("/{list_name}/picture/", response_model=schemas.RestaurantList, summary="create/update list cover photo")
async def update_picture(list_name: str, 
    user: models.Users = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db),
    picture: UploadFile = File(None)
):
    list = read_list(db=db, list_name=list_name, current_user=user)

    db_picture = await utils.create_picture(
        rating_id=None,
        picture=picture,
        owner_id=user.id,  # type: ignore
        db=db,
    )
    list.cover_picture = db_picture
    db.add(list)
    db.commit()
    db.refresh(list)
    return list