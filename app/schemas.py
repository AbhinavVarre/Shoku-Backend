from pydantic import BaseModel, ConfigDict

class RatingBase(BaseModel):
    score: int
    restaurant_id: int
    review: str | None = None

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    restaurant_id: int
    score: int
    review: str | None = None


class RestaurantBase(BaseModel):
    name: str

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    #list_id: int
    ratings: list[Rating] = []

class PictureBase(BaseModel):
    picture: bytes

class PictureCreate(PictureBase):
    pass
 
class Picture(PictureBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    owner_id: int
    rating_id: int

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
    #pictures: list['Picture'] = []  