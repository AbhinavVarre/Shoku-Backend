# -*- encoding: utf-8 -*-
# begin

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Unicode, Binary, LargeBinary, Time, DateTime, Date, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship, backref, deferred
from sqlalchemy.orm import sessionmaker

Base = declarative_base()



class Users (Base):
    __tablename__ = "users"
    user_id = Column('user_id', Integer, primary_key = True)
    name = Column('name', Unicode)
    password = Column('password', Unicode)

class Ratings (Base):
    __tablename__ = "ratings"
    rating_id = Column('rating_id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.user_id'))
    restaurant_id = Column('restaurant_id', Integer, ForeignKey('restaurants.restaurant_id'))
    date = Column('date', Date)

    users = relationship('Users', foreign_keys=owner_id)
    restaurants = relationship('Restaurants', foreign_keys=restaurant_id)

class Reviews (Base):
    __tablename__ = "reviews"
    review_id = Column('review_id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.user_id'))
    score = Column('score', Integer)

    users = relationship('Users', foreign_keys=owner_id)

class Restaurants (Base):
    __tablename__ = "restaurants"
    restaurant_id = Column('restaurant_id', Integer, primary_key = True)
    totalscore = Column('totalscore', Integer)
    numratings = Column('numRatings', Integer)
    list_id = Column('list_id', Integer, ForeignKey('restaurant_lists.list_id'))

    restaurant_lists = relationship('RestaurantLists', foreign_keys=list_id)

class Pictures (Base):
    __tablename__ = "pictures"
    picture_id = Column('picture_id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.user_id'))
    rating_id = Column('rating_id', Integer, ForeignKey('ratings.rating_id'))
    picture = Column('picture', LargeBinary)

    users = relationship('Users', foreign_keys=owner_id)
    ratings = relationship('Ratings', foreign_keys=rating_id)

class RestaurantLists (Base):
    __tablename__ = "restaurant_lists"
    list_id = Column('list_id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.user_id'))
    name = Column('name', Unicode)
    description = Column('description', Unicode)

    users = relationship('Users', foreign_keys=owner_id)

# end
