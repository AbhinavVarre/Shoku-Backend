from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from mangum import Mangum
import os


from . import crud, models, schemas
from .database import get_db
from .routers import auth, users, restaurants, ratings, lists, tags

#models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "authentication",
        "description": "Login function",
    },
    {
        "name": "users",
        "description": "Operations with users",
    },
    {
        "name": "ratings",
        "description": "Add  and read ratings",
    },
    {
        "name": "restaurants",
        "description": "Create and manage restaurants",
    },
    {
        "name": "lists",
        "description": "Create, upload to, and delete from lists.",
    },
    {
        "name": "tags",
        "description": "Create, upload to, and delete from tags.",
    },
]

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(openapi_tags=tags_metadata)

#including routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(ratings.router)
app.include_router(lists.router)
app.include_router(tags.router)


#CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

handler = Mangum(app)







