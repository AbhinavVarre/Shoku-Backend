from pydantic import BaseModel

class RatingBase(BaseModel):
    score: int
    restaurant_id: int

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
    ratings: list[Rating] = []
    #pictures: list['Picture'] = []  

    class Config:
        orm_mode = True


class RestaurantBase(BaseModel):
    name: str

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int
    totalscore: int
    numratings: int
    list_id: int
    ratings: list[Rating] = []

    class Config:
        orm_mode = True

class PictureBase(BaseModel):
    picture: bytes

class PictureCreate(PictureBase):
    pass

class Picture(PictureBase):
    id: int
    owner_id: int
    rating_id: int

    class Config:
        orm_mode = True

class RestaurantListBase(BaseModel):
    owner_id: int
    name: str
    description: str

class RestaurantListCreate(RestaurantListBase):
    pass

class RestaurantList(RestaurantListBase):
    id: int
    restaurants: list[Restaurant] = []

    class Config:
        orm_mode = True
