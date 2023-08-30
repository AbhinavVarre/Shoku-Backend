from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db

import os
from dotenv import load_dotenv

load_dotenv()

host     = os.getenv('HOST')
user     = os.getenv('DBUSER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
port     = os.getenv('PORT')

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:
            db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        db = None
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            if db:
                db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
