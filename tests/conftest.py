import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the parent directory to path so we can import the app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.client.database import Base, get_db
from app.schemas.users import User as UserSchema

# Create a test database
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    #Create a clean database for each test

    # Create the test database and tables
    Base.metadata.create_all(bind=engine)

    # Create a session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    #Create a test client using the test database


    # Override the get_db dependency
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Remove the override after the test
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def test_user(db):
    #Create a test user in the database

    user = UserSchema(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        role="user",
        active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_admin(db):
    #Create a test admin in the database

    admin = UserSchema(
        username="adminuser",
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        role="admin",
        active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def test_inactive_user(db):
    #Create an inactive test user in the database

    user = UserSchema(
        username="inactiveuser",
        email="inactive@example.com",
        first_name="Inactive",
        last_name="User",
        role="user",
        active=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
