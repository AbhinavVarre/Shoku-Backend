from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func,
    Date,
    Text,
    Boolean,
    Float,
    JSON,
)
from sqlalchemy.orm import relationship, backref, deferred
from .database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


# Many to many relationship between restaurants and restaurant lists
restaurant_association = Table(
    "restaurant_list_association",
    Base.metadata,
    Column(
        "restaurant_id",
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        primary_key=True,
    ),
    Column(
        "restaurant_list_id",
        UUID(as_uuid=True),
        ForeignKey("restaurant_lists.id"),
        primary_key=True,
    ),
)

# Many to many relationship between restaurants and tags
tag_association = Table(
    "tag_association",
    Base.metadata,
    Column(
        "restaurant_id",
        UUID(as_uuid=True),
        ForeignKey("restaurants.id"),
        primary_key=True,
    ),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), primary_key=True),
)

# Many to many relationship between lists and users
list_user_association = Table(
    "list_user_association",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column(
        "list_id",
        UUID(as_uuid=True),
        ForeignKey("restaurant_lists.id"),
        primary_key=True,
    ),
)

# Association Table
followers_association = Table(
    "followers_association",
    Base.metadata,
    Column("follower_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("followed_id", UUID(as_uuid=True), ForeignKey("users.id")),
)


class Users(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column("name", String)
    password = Column("password", String)
    created_at = Column("created_at", DateTime, default=func.now())

    ratings = relationship("Ratings", back_populates="user")
    pictures = relationship("Pictures", back_populates="user")

    lists = relationship(
        "RestaurantLists", secondary=list_user_association, back_populates="users"
    )

    followed = relationship(
        "Users",
        secondary=followers_association,
        primaryjoin=(followers_association.c.follower_id == id),
        secondaryjoin=(followers_association.c.followed_id == id),
        backref=backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )


class Ratings(Base):
    __tablename__ = "ratings"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    owner_id = Column("owner_id", UUID(as_uuid=True), ForeignKey("users.id"))
    restaurant_id = Column(
        "restaurant_id", UUID(as_uuid=True), ForeignKey("restaurants.id")
    )
    created_at = Column("created_at", DateTime, default=func.now())
    score = Column("score", Integer)
    review = Column("review", String)

    user = relationship("Users", back_populates="ratings")
    restaurant = relationship("Restaurants", back_populates="ratings")
    pictures = relationship("Pictures", back_populates="rating")


class Pictures(Base):
    __tablename__ = "pictures"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    owner_id = Column("owner_id", UUID(as_uuid=True), ForeignKey("users.id"))
    rating_id = Column("rating_id", UUID(as_uuid=True), ForeignKey("ratings.id"))
    pictureUrl = Column("pictureURL", String)
    created_at = Column("created_at", DateTime, default=func.now())

    user = relationship("Users", back_populates="pictures")
    rating = relationship("Ratings", back_populates="pictures")
    restaurant_list = relationship("RestaurantLists", back_populates="cover_picture")


class Restaurants(Base):
    __tablename__ = "restaurants"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column("name", String)
    created_at = Column("created_at", DateTime, default=func.now())
    # list_id = Column('list_id', UUID(as_uuid=True), ForeignKey('restaurant_lists.id'))

    ratings = relationship("Ratings", back_populates="restaurant")
    lists = relationship(
        "RestaurantLists",
        secondary=restaurant_association,
        back_populates="restaurants",
    )

    tags = relationship("Tags", secondary=tag_association, back_populates="restaurants")


class RestaurantLists(Base):
    __tablename__ = "restaurant_lists"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column("name", String)
    description = Column("description", String)
    cover_picture_id = Column(
        "cover_picture_id", UUID(as_uuid=True), ForeignKey("pictures.id")
    )
    created_at = Column("created_at", DateTime, default=func.now())

    cover_picture = relationship("Pictures", back_populates="restaurant_list")

    restaurants = relationship(
        "Restaurants", secondary=restaurant_association, back_populates="lists"
    )

    users = relationship(
        "Users", secondary=list_user_association, back_populates="lists"
    )

    @property
    def user_names(self):
        return [user.name for user in self.users]


class Tags(Base):
    __tablename__ = "tags"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column("name", String)
    created_at = Column("created_at", DateTime, default=func.now())

    restaurants = relationship(
        "Restaurants", secondary=tag_association, back_populates="tags"
    )

    @property
    def restaurant_names(self):
        return [restaurant.name for restaurant in self.restaurants]
