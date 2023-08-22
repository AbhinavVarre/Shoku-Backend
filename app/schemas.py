from typing import List, Union

from pydantic import BaseModel

class RatingBase(BaseModel):
    score: int
    restaurant_id: int
    owner_id: int

class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    id: int
    owner_id: int
    restaurant_id: int
    score: int
    date: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    password: str

class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    ratings: List[Rating] = []
    #reviews: List['Review'] = []
    #pictures: List['Picture'] = []  

    class Config:
        orm_mode = True

