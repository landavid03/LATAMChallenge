from fastapi import APIRouter, Depends, Query, Path, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.client.database import get_db
from app.models.users import User, UserCreate, UserUpdate
from app.crud import users as user_crud
from app.api.errors import UserNotFoundException, UserAlreadyExistsException

# Create logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)


@router.post(
    "/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information"
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new user with all the necessary information:

    - **username**: unique username (3-50 characters)
    - **email**: unique email address
    - **first_name**: first name (1-50 characters)
    - **last_name**: last name (1-50 characters)
    - **role**: role (admin, user, or guest)
    - **active**: whether the user is active
    """
    # Check if user with same email exists
    existing_email = user_crud.get_user_by_email(db, user.email)
    if existing_email:
        logger.warning(f"Attempt to create user with existing email: {user.email}")
        raise UserAlreadyExistsException(detail="User with this email already exists")

    # Check if user with same username exists
    existing_username = user_crud.get_user_by_username(db, user.username)
    if existing_username:
        logger.warning(f"Attempt to create user with existing username: {user.username}")
        raise UserAlreadyExistsException(detail="User with this username already exists")

    logger.info(f"Creating new user with username: {user.username}")
    return user_crud.create_user(db, user)


@router.get(
    "/",
    response_model=List[User],
    summary="Get all users",
    description="Get a list of all users with optional pagination and filtering"
)
def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return"),
    active_only: bool = Query(False, description="Only return active users"),
    db: Session = Depends(get_db)
):
    """
    Get a list of users with pagination:

    - **skip**: number of users to skip (for pagination)
    - **limit**: maximum number of users to return
    - **active_only**: if true, only return active users
    """
    logger.info(f"Getting users with skip={skip}, limit={limit}, active_only={active_only}")
    return user_crud.get_users(db, skip=skip, limit=limit, active_only=active_only)


@router.get(
    "/{user_id}",
    response_model=User,
    summary="Get a specific user",
    description="Get details for a specific user by ID"
)
def get_user(
    user_id: int = Path(..., ge=1, description="The ID of the user to get"),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID:

    - **user_id**: ID of the user to retrieve
    """
    logger.info(f"Getting user with id={user_id}")
    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        logger.warning(f"User not found with id={user_id}")
        raise UserNotFoundException()
    return db_user


@router.put(
    "/{user_id}",
    response_model=User,
    summary="Update a user",
    description="Update a user's information"
)
def update_user(
    user_update: UserUpdate,
    user_id: int = Path(..., ge=1, description="The ID of the user to update"),
    db: Session = Depends(get_db)
):
    """
    Update a user's information:

    - **user_id**: ID of the user to update
    - **user_update**: Fields to update (only include fields you want to change)
    """
    logger.info(f"Updating user with id={user_id}")

    # Check if username is being updated and if it already exists
    if user_update.username:
        existing_user = user_crud.get_user_by_username(db, user_update.username)
        if existing_user and existing_user.id != user_id:
            logger.warning(f"Cannot update user {user_id}: username {user_update.username} already exists")
            raise UserAlreadyExistsException(detail="User with this username already exists")

    # Check if email is being updated and if it already exists
    if user_update.email:
        existing_user = user_crud.get_user_by_email(db, user_update.email)
        if existing_user and existing_user.id != user_id:
            logger.warning(f"Cannot update user {user_id}: email {user_update.email} already exists")
            raise UserAlreadyExistsException(detail="User with this email already exists")

    updated_user = user_crud.update_user(db, user_id, user_update)
    if not updated_user:
        logger.warning(f"User not found with id={user_id}")
        raise UserNotFoundException()

    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Delete a specific user by ID"
)
def delete_user(
    user_id: int = Path(..., ge=1, description="The ID of the user to delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a user by ID:

    - **user_id**: ID of the user to delete
    """
    logger.info(f"Deleting user with id={user_id}")
    success = user_crud.delete_user(db, user_id)
    if not success:
        logger.warning(f"User not found with id={user_id}")
        raise UserNotFoundException()

    return None
