from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Optional
import os
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

# Configuration for password hashing
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration for JWT tokens
# TODO: Move these to environment variables and a config file
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "your-super-secret-key-for-jwt") # KEEP THIS SECRET!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", "30")) # Default 30 minutes

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

