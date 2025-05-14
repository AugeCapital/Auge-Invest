from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import database as db_config
from ..schemas import user_schemas
from ..crud import user_crud
from ..utils import security # Assuming you'll have a get_current_active_user function here

router = APIRouter()

# Placeholder for dependency to get current user
# This would typically involve decoding a JWT token from the Authorization header
async def get_current_active_user(token: str = Depends(security.oauth2_scheme), db: Session = Depends(db_config.get_db)) -> user_schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = security.decode_token(token)
    if payload is None:
        raise credentials_exception
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    user = user_crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    # TODO: Add check for user.is_active if that field is implemented
    return user_schemas.User.from_orm(user) # Ensure Pydantic model conversion


@router.get("/me", response_model=user_schemas.User)
async def read_users_me(current_user: user_schemas.User = Depends(get_current_active_user)):
    """
    Get current logged-in user.
    """
    return current_user

# TODO: Add other user-related endpoints if necessary (e.g., update user profile)

