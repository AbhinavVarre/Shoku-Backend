from sqlalchemy import Table, Column, Integer, BigInteger, String, ForeignKey, Unicode, LargeBinary, Time, DateTime, Date, Text, Boolean, Float, JSON
from sqlalchemy.orm import relationship, backref, deferred
from .database import Base



class Users (Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    password = Column('password', String)

    ratings = relationship('Ratings', back_populates='user')
    pictures = relationship('Pictures', back_populates='user')
    lists = relationship('RestaurantLists', back_populates='user')

class Ratings (Base):
    __tablename__ = "ratings"
    id = Column('id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'))
    restaurant_id = Column('restaurant_id', Integer, ForeignKey('restaurants.id'))
    created_at = Column('created_at', String)
    score = Column('score', Integer)
    review = Column('review', String)
    pictureUrl = Column('pictureURL', String)

    user = relationship('Users', back_populates='ratings')
    restaurant = relationship('Restaurants', back_populates='ratings')
    pictures = relationship('Pictures', back_populates='review')

class Pictures (Base):
    __tablename__ = "pictures"
    id = Column('id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'))
    rating_id = Column('rating_id', Integer, ForeignKey('ratings.id'))
    picture = Column('picture', LargeBinary)

    user = relationship('Users', back_populates='pictures')
    review = relationship('Ratings', back_populates='pictures')

# Many to many relationship between restaurants and restaurant lists
restaurant_association = Table(
    'restaurant_list_association',
    Base.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurants.id'), primary_key=True),
    Column('restaurant_list_id', Integer, ForeignKey('restaurant_lists.id'), primary_key=True)
)

# Many to many relationship between restaurants and tags
tag_association = Table('tag_association', Base.metadata,
    Column('restaurant_id', Integer, ForeignKey('restaurants.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Restaurants (Base):
    __tablename__ = "restaurants"
    id = Column('id', Integer, primary_key = True)
    name = Column('name', String)
    #list_id = Column('list_id', Integer, ForeignKey('restaurant_lists.id'))

    ratings = relationship('Ratings', back_populates='restaurant')
    lists = relationship( 
        'RestaurantLists',
        secondary=restaurant_association,
        back_populates='restaurants'
    )

    tags = relationship(
        'Tags',
        secondary=tag_association,
        back_populates='restaurants'
    )

class RestaurantLists (Base):
    __tablename__ = "restaurant_lists"
    id = Column('id', Integer, primary_key = True)
    owner_id = Column('owner_id', Integer, ForeignKey('users.id'))
    name = Column('name', String)
    description = Column('description', String)

    user = relationship('Users', back_populates='lists')
    restaurants = relationship(
        'Restaurants', 
        secondary=restaurant_association,
        back_populates='lists' 
    )

class Tags(Base):
    __tablename__ = "tags"
    
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    
    restaurants = relationship(
        'Restaurants', 
        secondary=tag_association,
        back_populates='tags'
    )

