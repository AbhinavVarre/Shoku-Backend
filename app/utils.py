from passlib.context import CryptContext
from fastapi import UploadFile, HTTPException,status
import boto3
import os
from dotenv import load_dotenv
from urllib.parse import quote
import magic

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
allowed_mimes = {'image/png', 
                 'image/jpeg', 
                 'image/gif'}

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

load_dotenv()
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION")

async def upload_file_to_s3 (file: UploadFile):

    #check file size
    contents = await file.read()
    size = len(contents)
    MB = 1024**2
    if not 0 <size<=5*MB:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail="File size must be between 1 and 5 MB")

    #check file MIME type
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.file.read(1024))  # Read only the first 1024 bytes to determine MIME type
    file.file.seek(0)  # Reset file pointer
    if file_mime_type not in allowed_mimes:
         raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail=f'Unsupported file type: {file_mime_type}. Supprted types are: {allowed_mimes}')

    #upload file to S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )
    s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, file.filename)
    file_key = quote(file.filename, safe='') # type: ignore
    url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{file_key}"
    return url

