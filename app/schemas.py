from typing import List, Union

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    password: str


class User(UserBase):
    id: int
    ratings: List['Rating'] = []
    #reviews: List['Review'] = []
    #pictures: List['Picture'] = []  

    class Config:
        orm_mode = True

class RatingBase(BaseModel):
    score: int
    restaurant_id: int
    owner_id: int


class Rating(UserBase):
    id: int
    owner_id: int
    restaurant_id: int
    score: int
    date: str

    class Config:
        orm_mode = True