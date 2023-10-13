from passlib.context import CryptContext
from fastapi import UploadFile, HTTPException, status, File, Depends
import boto3
import os
from dotenv import load_dotenv
from urllib.parse import quote
from . import models
from .database import get_db
from sqlalchemy.orm import Session
import datetime
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
allowed_mimes = {"image/png", "image/jpeg"}


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


load_dotenv()
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION")


async def create_picture(
    owner_id: UUID,
    rating_id: UUID | None = None,
    picture: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    pictureUrl = await upload_file_to_s3(picture)
    db_picture = models.Pictures(
        rating_id=rating_id, owner_id=owner_id, pictureUrl=pictureUrl
    )
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    return db_picture


async def upload_file_to_s3(file: UploadFile):
    # check file size
    contents = await file.read()
    size = len(contents)
    MB = 1024**2
    if not 0 < size <= 5 * MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be between 1 and 5 MB",
        )
    await file.seek(0)

    # check file MIME type
    file_mime_type = file.content_type
    if file_mime_type not in allowed_mimes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file_mime_type}. Supprted types are: {allowed_mimes}",
        )

    # upload file to S3
    s3_client = boto3.client(
        "s3", aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY
    )
    s3_client.upload_fileobj(
        file.file,
        S3_BUCKET_NAME,
        file.filename,
        ExtraArgs={"ContentDisposition": "attachment"},
    )
    file_key = quote(file.filename, safe="")  # type: ignore
    url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{file_key}"
    return url
