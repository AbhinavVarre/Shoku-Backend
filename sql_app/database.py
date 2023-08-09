from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#to encode as environment variable
host     = "shoku-dev.c8iml9o89lxg.us-east-2.rds.amazonaws.com"
user     = "postgres"
password = "shokudevdb"
database = "postgres"
port     = 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()