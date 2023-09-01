from passlib.context import CryptContext
from fastapi import UploadFile
import boto3
import os
from dotenv import load_dotenv


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

load_dotenv()
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_REGION = os.getenv("S3_REGION")

def upload_file_to_s3 (file: UploadFile):
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY
    )

    s3_client.upload_fileobj(file.file, S3_BUCKET_NAME, file.filename)

    #url = s3_client.generate_presigned_url(
    #    ClientMethod='get_object',
    #    Params={ 
    #        'Bucket': S3_BUCKET_NAME,
    #        'Key': file.filename
    #    }
    #)
    url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{file.filename}"
    return url

