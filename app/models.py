from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Unicode, LargeBinary, Time, DateTime, Date, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship, backref, deferred
from .database import Base



class Users (Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    password = Column('password', String)

    ratings = relationship('Ratings', back_populates='user')
    reviews = relationship('Reviews', back_populates='user')
    pictures = relationship('Pictures', back_populates='user')
    lists = relationship('RestaurantLists', back_populates='user')

class Ratings (Base):
    __tablename__ = "ratings"
    id = Column('id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'))
    restaurant_id = Column('restaurant_id', Integer, ForeignKey('restaurants.id'))
    date = Column('date', Date)
    score = Column('score', Integer)

    user = relationship('Users', back_populates='ratings')
    restaurant = relationship('Restaurants', back_populates='ratings')

class Reviews (Base):
    __tablename__ = "reviews"
    id = Column('id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'))
    date = Column('date', Date)
    review = Column('review', String)
    
    user = relationship('Users', back_populates='reviews')
    pictures = relationship('Pictures', back_populates='review')

class Restaurants (Base):
    __tablename__ = "restaurants"
    id = Column('id', Integer, primary_key = True)
    totalscore = Column('totalscore', Integer)
    numratings = Column('numRatings', Integer)
    list_id = Column('list_id', Integer, ForeignKey('restaurant_lists.id'))

    ratings = relationship('Ratings', back_populates='restaurant')
    restaurant_list = relationship('RestaurantLists', back_populates='restaurants')

class Pictures (Base):
    __tablename__ = "pictures"
    id = Column('id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'))
    rating_id = Column('rating_id', Integer, ForeignKey('reviews.id'))
    picture = Column('picture', LargeBinary)

    user = relationship('Users', back_populates='pictures')
    review = relationship('Reviews', back_populates='pictures')

class RestaurantLists (Base):
    __tablename__ = "restaurant_lists"
    id = Column('id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'))
    name = Column('name', String)
    description = Column('description', String)

    user = relationship('Users', back_populates='lists')
    restaurants = relationship('Restaurants', back_populates='restaurant_list')
