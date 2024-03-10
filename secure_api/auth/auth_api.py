from datetime import datetime, timedelta

from typing import List
from pydantic import EmailStr
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from secure_api.database.database import get_session
from secure_api.models import models
from secure_api import configs


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(session: Session, email: EmailStr):
    return session.exec(select(models.User).where(models.User.email == email)).first()

def authenticate_user(session: Session, email: EmailStr, password: str):
    user = get_user(session, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username", headers={"WWW-Authenticate": "Bearer"})
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, configs.JWT_SECRET, algorithm=configs.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, configs.JWT_SECRET, algorithms=configs.JWT_ALGORITHM)
        email: EmailStr = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = models.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"},)
    return verify_token(token, credentials_exception=credentials_exception)

def get_current_active_user(current_user: models.User = Depends(get_current_user),):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
