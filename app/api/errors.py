from fastapi import HTTPException, status
from typing import Dict, Any, Optional


class UserNotFoundException(HTTPException):
    #Exception raised when a user is not found
    def __init__(
        self,
        detail: str = "User not found",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            headers=headers,
        )


class UserAlreadyExistsException(HTTPException):
    #Exception raised when attempting to create a user that already exists
    def __init__(
        self,
        detail: str = "User with this username or email already exists",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            headers=headers,
        )


class InvalidUserDataException(HTTPException):
    #Exception raised when user data is invalid
    def __init__(
        self,
        detail: str = "Invalid user data",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            headers=headers,
        )
