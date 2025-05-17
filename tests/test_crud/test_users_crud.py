import pytest
from datetime import datetime
from app.crud import users as user_crud
from app.models.users import UserCreate, UserUpdate
from app.schemas.users import User as UserSchema


def test_get_user(db, test_user):
    #Test getting a user by ID"""
    user = user_crud.get_user(db, test_user.id)
    assert user is not None
    assert user.id == test_user.id
    assert user.username == test_user.username
    assert user.email == test_user.email


def test_get_user_not_found(db):
    #Test getting a non-existent user"""
    user = user_crud.get_user(db, 999)  # Non-existent ID
    assert user is None


def test_get_user_by_email(db, test_user):
    #Test getting a user by email"""
    user = user_crud.get_user_by_email(db, test_user.email)
    assert user is not None
    assert user.id == test_user.id
    assert user.email == test_user.email


def test_get_user_by_email_not_found(db):
    #Test getting a user by non-existent email"""
    user = user_crud.get_user_by_email(db, "nonexistent@example.com")
    assert user is None


def test_get_user_by_username(db, test_user):
    #Test getting a user by username"""
    user = user_crud.get_user_by_username(db, test_user.username)
    assert user is not None
    assert user.id == test_user.id
    assert user.username == test_user.username


def test_get_user_by_username_not_found(db):
    #Test getting a user by non-existent username"""
    user = user_crud.get_user_by_username(db, "nonexistentuser")
    assert user is None


def test_get_users(db, test_user, test_admin, test_inactive_user):
    #Test getting all users"""
    users = user_crud.get_users(db)
    assert len(users) == 3  # All users including inactive

    # Test with active_only filter
    active_users = user_crud.get_users(db, active_only=True)
    assert len(active_users) == 2  # Only active users

    # Test with pagination
    paginated_users = user_crud.get_users(db, skip=1, limit=1)
    assert len(paginated_users) == 1  # Only one user due to limit


def test_create_user(db):
    #Test creating a new user"""
    user_create = UserCreate(
        username="newuser",
        email="new@example.com",
        first_name="New",
        last_name="User",
        role="user",
        active=True
    )

    user = user_crud.create_user(db, user_create)

    assert user is not None
    assert user.id is not None
    assert user.username == user_create.username
    assert user.email == user_create.email
    assert user.first_name == user_create.first_name
    assert user.last_name == user_create.last_name
    assert user.role == user_create.role
    assert user.active == user_create.active
    assert user.created_at is not None
    assert user.updated_at is not None


def test_update_user(db, test_user):
    #Test updating an existing user"""
    user_update = UserUpdate(
        first_name="Updated",
        last_name="Name",
        active=False
    )

    updated_user = user_crud.update_user(db, test_user.id, user_update)

    assert updated_user is not None
    assert updated_user.id == test_user.id
    assert updated_user.first_name == user_update.first_name
    assert updated_user.last_name == user_update.last_name
    assert updated_user.active == user_update.active
    # These should not change
    assert updated_user.username == test_user.username
    assert updated_user.email == test_user.email

    # Verify update in database
    db_user = user_crud.get_user(db, test_user.id)
    assert db_user.first_name == user_update.first_name
    assert db_user.last_name == user_update.last_name
    assert db_user.active == user_update.active


def test_update_user_not_found(db):
    #Test updating a non-existent user"""
    user_update = UserUpdate(first_name="Updated")

    updated_user = user_crud.update_user(db, 999, user_update)  # Non-existent ID

    assert updated_user is None


def test_delete_user(db, test_user):
    #Test deleting a user"""
    result = user_crud.delete_user(db, test_user.id)

    assert result is True

    # Verify user is gone
    db_user = user_crud.get_user(db, test_user.id)
    assert db_user is None


def test_delete_user_not_found(db):
    #Test deleting a non-existent user"""
    result = user_crud.delete_user(db, 999)  # Non-existent ID

    assert result is False
