from pydantic import BaseModel, ConfigDict
from fastapi import UploadFile
from typing import ForwardRef


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None

class RatingBase(BaseModel):
    score: int
    restaurant_id: int
    review: str | None = None

class RatingCreate(RatingBase):
    pass

class PictureBase(BaseModel):
    pictureUrl: str

class PictureCreate(PictureBase):
    pass
 
class Picture(PictureBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    rating_id: int

class Rating(RatingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    restaurant_id: int
    score: int
    created_at: str | None = None
    pictures: list[Picture] = []  
    review: str | None = None


class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    #restaurants: list[Restaurant] = []


class RestaurantBase(BaseModel):
    name: str

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    ratings: list[Rating] = []
    tags: list[Tag] = []

class RestaurantListBase(BaseModel):
    name: str
    description: str

class RestaurantListCreate(RestaurantListBase):
    pass

class RestaurantList(RestaurantListBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    restaurants: list[Restaurant] = []

class UserBase(BaseModel):
    name: str
    password: str

class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    ratings: list[Rating] = []
    lists: list[RestaurantList] = []
    pictures: list[Picture] = []  