from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Unicode, Binary, LargeBinary, Time, DateTime, Date, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship, backref, deferred
from .database import Base



class Users (Base):
    __tablename__ = "users"
    user_id = Column('user_id', Integer, primary_key = True)
    name = Column('name', String)
    password = Column('password', String)

    ratings = relationship('Ratings', back_populates='user')
    reviews = relationship('Reviews', back_populates='user')
    pictures = relationship('Pictures', back_populates='user')

class Ratings (Base):
    __tablename__ = "ratings"
    id = Column('rating_id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.user_id'))
    restaurant_id = Column('restaurant_id', Integer, ForeignKey('restaurants.restaurant_id'))
    date = Column('date', Date)
    score = Column('score', Integer)

    user = relationship('Users', back_populates='ratings')
    restaurant = relationship('Restaurants', back_populates='ratings')

class Reviews (Base):
    __tablename__ = "reviews"
    id = Column('review_id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.user_id'))
    date = Column('date', Date)
    review = Column('review', String)
    
    user = relationship('Users', back_populates='reviews')
    picture = relationship('Pictures', back_populates='review')

class Restaurants (Base):
    __tablename__ = "restaurants"
    id = Column('restaurant_id', Integer, primary_key = True)
    totalscore = Column('totalscore', Integer)
    numratings = Column('numRatings', Integer)
    list_id = Column('list_id', Integer, ForeignKey('restaurant_lists.list_id'))

    ratings = relationship('Ratings', back_populates='restaurant')
    restaurant_list = relationship('RestaurantLists', back_populates='restaurants')

class Pictures (Base):
    __tablename__ = "pictures"
    id = Column('picture_id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.user_id'))
    rating_id = Column('rating_id', Integer, ForeignKey('ratings.rating_id'))
    picture = Column('picture', LargeBinary)

    user = relationship('Users', back_populates='pictures')
    review = relationship('Reviews', back_populates='pictures')

class RestaurantLists (Base):
    __tablename__ = "restaurant_lists"
    id = Column('list_id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.user_id'))
    name = Column('name', String)
    description = Column('description', String)

    users = relationship('Users', back_populates=owner_id)
    restaurants = relationship('RestaurantLists', back_populates='restaurant_list')

