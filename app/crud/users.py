from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.schemas.users import User as UserSchema
from app.models.users import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[UserSchema]:
#    Get a user by ID
    return db.query(UserSchema).filter(UserSchema.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserSchema]:
    #Get a user by email
    return db.query(UserSchema).filter(UserSchema.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[UserSchema]:
    #Get a user by username
    return db.query(UserSchema).filter(UserSchema.username == username).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False
) -> List[UserSchema]:
    #Get multiple users with pagination
    query = db.query(UserSchema)
    if active_only:
        query = query.filter(UserSchema.active == True)

    return query.offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> UserSchema:
    #Create a new user

    db_user = UserSchema(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        active=user.active,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(
    db: Session,
    user_id: int,
    user_update: UserUpdate
) -> Optional[UserSchema]:

    #Update an existing user

    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db_user.updated_at = datetime.utcnow()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:

    #Delete a user

    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True
