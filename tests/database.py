from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db
from alembic import command
from alembic.config import Config

import os
from dotenv import load_dotenv

load_dotenv()

host     = os.getenv('HOST')
user     = os.getenv('DBUSER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
port     = os.getenv('PORT')

SQLALCHEMY_TEST_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}_test"

engine = create_engine(SQLALCHEMY_TEST_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

alembic_cfg = Config("alembic.ini")

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #command.downgrade(alembic_cfg, "base")
    #command.upgrade(alembic_cfg, "head")
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
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
