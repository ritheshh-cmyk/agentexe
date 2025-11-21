from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

def get_private_key():
    with open("server/private_key.pem", "rb") as f:
        return f.read()

def get_public_key():
    with open("server/public_key.pem", "rb") as f:
        return f.read()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    private_key = get_private_key()
    encoded_jwt = jwt.encode(to_encode, private_key, algorithm=ALGORITHM)
    return encoded_jwt, expire
