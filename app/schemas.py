from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile
from typing import ForwardRef
from datetime import datetime
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: UUID | None = None

class RatingBase(BaseModel):
    score: int
    review: str | None = None

class RatingCreate(RatingBase):
    restaurant_name: str

class PictureBase(BaseModel):
    pictureUrl: str

class PictureCreate(PictureBase):
    pass
 
class Picture(PictureBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    owner_id: UUID
    rating_id: UUID
    created_at: datetime | None = None

class Rating(RatingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    owner_id: UUID
    restaurant_id: UUID
    score: int
    created_at: datetime | None = None
    pictures: list[Picture] = []  
    review: str | None = None


class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    restaurant_names: list['str'] = []


class RestaurantBase(BaseModel):
    name: str

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    ratings: list[Rating] = []
    tags: list[Tag] = []

class RestaurantListBase(BaseModel):
    name: str
    description: str

class RestaurantListCreate(RestaurantListBase):
    pass

class RestaurantList(RestaurantListBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    restaurants: list[Restaurant] = []
    user_names: list[str] = []

class UserBase(BaseModel):
    name: str
    password: str

class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    ratings: list[Rating] = []
    lists: list[RestaurantList] = []
    pictures: list[Picture] = []  