import pytest
from fastapi import status
import json
from datetime import datetime


def test_create_user(client):
    """Test creating a new user"""
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "User",
        "role": "user",
        "active": True
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["role"] == user_data["role"]
    assert data["active"] == user_data["active"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_user_duplicate_username(client, test_user):
    """Test creating a user with a duplicate username"""
    user_data = {
        "username": test_user.username,  # Already exists
        "email": "unique@example.com",
        "first_name": "Unique",
        "last_name": "User",
        "role": "user",
        "active": True
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]


def test_create_user_duplicate_email(client, test_user):
    """Test creating a user with a duplicate email"""
    user_data = {
        "username": "uniqueuser",
        "email": test_user.email,  # Already exists
        "first_name": "Unique",
        "last_name": "User",
        "role": "user",
        "active": True
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]


def test_create_user_invalid_data(client):
    """Test creating a user with invalid data"""
    # Test with missing fields
    user_data = {
        "username": "invaliduser",
        "email": "invalid@example.com"
        # Missing required fields
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_users(client, test_user, test_admin, test_inactive_user):
    """Test getting all users"""
    response = client.get("/api/v1/users/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3  # All users including inactive

    # Test with active_only filter
    response = client.get("/api/v1/users/?active_only=true")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2  # Only active users

    # Test with pagination
    response = client.get("/api/v1/users/?skip=1&limit=1")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1  # Only one user due to limit


def test_get_user_by_id(client, test_user):
    """Test getting a user by ID"""
    response = client.get(f"/api/v1/users/{test_user.id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email


def test_get_user_not_found(client):
    """Test getting a non-existent user"""
    response = client.get("/api/v1/users/999")  # Non-existent ID

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"]


def test_update_user(client, test_user):
    """Test updating a user"""
    update_data = {
        "first_name": "Updated",
        "last_name": "Name",
        "active": False
    }

    response = client.put(f"/api/v1/users/{test_user.id}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_user.id
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["active"] == update_data["active"]
    # These should not change
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email


def test_update_user_not_found(client):
    """Test updating a non-existent user"""
    update_data = {
        "first_name": "Updated"
    }

    response = client.put("/api/v1/users/999", json=update_data)  # Non-existent ID

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"]


def test_update_user_duplicate_username(client, test_user, test_admin):
    """Test updating a user with a duplicate username"""
    update_data = {
        "username": test_admin.username  # Already exists
    }

    response = client.put(f"/api/v1/users/{test_user.id}", json=update_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]


def test_update_user_duplicate_email(client, test_user, test_admin):
    """Test updating a user with a duplicate email"""
    update_data = {
        "email": test_admin.email  # Already exists
    }

    response = client.put(f"/api/v1/users/{test_user.id}", json=update_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]


def test_delete_user(client, test_user):
    """Test deleting a user"""
    response = client.delete(f"/api/v1/users/{test_user.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify user is gone
    response = client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_not_found(client):
    """Test deleting a non-existent user"""
    response = client.delete("/api/v1/users/999")  # Non-existent ID

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"]
