from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from ..db import database as db_config
from ..schemas import user_schemas
from ..utils import security
from ..crud import user_crud # To be created

router = APIRouter()

@router.post("/register", response_model=user_schemas.User, status_code=status.HTTP_201_CREATED)
async def register_new_user(
    user_in: user_schemas.UserCreate,
    db: Session = Depends(db_config.get_db)
):
    """
    Register a new user.
    """
    db_user = user_crud.get_user_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    created_user = user_crud.create_user(db=db, user=user_in)
    return created_user

@router.post("/login/access-token", response_model=user_schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(db_config.get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = user_crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# TODO: Add endpoint for /users/me to get current user
# TODO: Add endpoint for token refresh if needed
# TODO: Add endpoint for password recovery/reset

