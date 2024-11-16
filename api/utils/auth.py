import os
import jwt
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from crud.veterinarian import get_veterinarian
# Carrega as variáveis de ambiente
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")



def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



