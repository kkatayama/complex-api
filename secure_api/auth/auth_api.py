from datetime import datetime, timedelta
from pathlib import Path
import json

from pydantic import ValidationError
from sqlmodel import Session
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from secure_api.database.database import get_session
from secure_api.models import models
from secure_api import configs


###############################################################################
#                          Password And JWT Functions                         #
###############################################################################


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str):
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)

def create_access_token(user_id, expires_delta: timedelta):
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = ({"exp": expire, "sub": user_id})
    encoded_jwt = jwt.encode(to_encode, configs.JWT_SECRET_KEY, algorithm=configs.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id, expires_delta: timedelta):
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=configs.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = ({"exp": expire, "sub": user_id})
    encoded_jwt = jwt.encode(to_encode, configs.JWT_REFRESH_KEY, algorithm=configs.JWT_ALGORITHM)
    return encoded_jwt


###############################################################################
#                         OAuth2 API Related Functions                        #
###############################################################################


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login",  scheme_name="JWT")


def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_session)):
    headers={"WWW-Authenticate": "Bearer"}
    # -- Verify Token --#
    try:
        payload = jwt.decode(token, configs.JWT_SECRET_KEY, algorithms=[configs.JWT_ALGORITHM])
        token_data = models.TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers=headers)
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token", headers=headers)

    user = db.get(models.User, token_data.sub)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")
    return user

def get_refresh_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_session)):
    headers={"WWW-Authenticate": "Bearer"}
    # -- Verify Token --#
    try:
        payload = jwt.decode(token, configs.JWT_REFRESH_KEY, algorithms=[configs.JWT_ALGORITHM])
        token_data = models.TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers=headers)
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token", headers=headers)

    user = db.get(models.User, token_data.sub)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")
    return user


###############################################################################
#                           Utility Helper Functions                          #
###############################################################################

# Dependency to check token revocation
# def is_token_revoked(token: str = Depends(reuseable_oauth)):
#     """
#     Dependency function to check if a token is revoked before processing a request.
#     """
#     if token in configs.revoked_tokens:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been revoked")
#     return token
