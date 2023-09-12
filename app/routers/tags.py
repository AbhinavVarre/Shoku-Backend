from fastapi import Depends, FastAPI, HTTPException, APIRouter
from app import schemas, models, crud
from ..database import get_db
from sqlalchemy.orm import Session
from .. import utils


router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


#Create a tag
@router.post("/add", response_model=schemas.Tag, summary="create a tag")
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = models.Tags( **tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

#get a tag by name
@router.get("/get/{name}", response_model=schemas.Tag, summary="Get a tag by name")
def read_tag(name: str, db: Session = Depends(get_db)):
    tag = (
        db.query(models.Tags).filter(models.Tags.name == name).first()
    )
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

#get all tags
@router.get("/get", response_model=list[schemas.Tag], summary="Get all tags")
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(models.Tags).offset(skip).limit(limit).all()
    return tags

#Tag a restaurant
@router.post("/{restaurant_name}/add/{tag_name}", response_model=schemas.Restaurant, summary="Tag a restaurant")
def tag_restaurant(restaurant_name: str, tag_name, db: Session = Depends(get_db)):
    restaurant = crud.read_restaurant(db, name=restaurant_name)
    tag = read_tag(db=db, name=tag_name)
    restaurant.tags.append(tag)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

#Read all restaurants associated with a tag
@router.get("/{tag_name}/restaurants", response_model=list[schemas.Restaurant],summary="Read all restaurants associated with a tag")
def get_restaurants_by_tag(tag_name: str, db: Session = Depends(get_db)):
    tag = read_tag(db=db, name=tag_name)
    return tag.restaurants

#Read all tags associated with a restaurant
@router.get("/{restaurant_name}/tags", response_model=list[schemas.Tag], summary="Read all tags associated with a restaurant")
def get_tags_by_restaurant(restaurant_name: str, db: Session = Depends(get_db)):
    restaurant = crud.read_restaurant(db, name=restaurant_name)
    return restaurant.tags