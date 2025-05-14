from sqlalchemy.orm import Session

from ..db import database as db_config # Alias to avoid conflict
from ..models import user_models # To be created, or use db_config.User if models are there
from ..schemas import user_schemas
from ..utils import security


def get_user(db: Session, user_id: int):
    return db.query(db_config.User).filter(db_config.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(db_config.User).filter(db_config.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_config.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = db_config.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> db_config.User | None:
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

# TODO: Add CRUD functions for updating user, deleting user, etc.

