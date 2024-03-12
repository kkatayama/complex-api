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
from secure_api.models.models import User
from secure_api.schemas.schemas import TokenPayload
from secure_api.configs import JWT_ALGORITHM, JWT_REFRESH_KEY, JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

from rich.console import Console
from rich import inspect


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
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = ({"exp": expire, "sub": str(user_id)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(user_id, expires_delta: timedelta):
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = ({"exp": expire, "sub": str(user_id)})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


###############################################################################
#                         OAuth2 API Related Functions                        #
###############################################################################


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login",  scheme_name="JWT")


c = Console()


def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_session)):
    headers={"WWW-Authenticate": "Bearer"}
    # -- Verify Token --#
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers=headers)
    except (JWTError, ValidationError) as ext:
        c.print(inspect(ext))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token", headers=headers)

    user = db.get(User, token_data.sub)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")
    return user

def get_refresh_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_session)):
    headers={"WWW-Authenticate": "Bearer"}
    # -- Verify Token --#
    try:
        payload = jwt.decode(token, JWT_REFRESH_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers=headers)
    except (JWTError, ValidationError) as ext:
        c.print(inspect(ext))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token", headers=headers)

    user = db.get(User, token_data.sub)
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

def get_access_token(token: str = Depends(reuseable_oauth), db: Session = Depends(get_session)):
    headers={"WWW-Authenticate": "Bearer"}
    # -- Verify Token --#
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers=headers)
    except (JWTError, ValidationError) as ext:
        c.print(inspect(ext))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token", headers=headers)
    return token_data

def get_refresh_token(token: str = Depends(reuseable_oauth), db: Session = Depends(get_session)):
    headers={"WWW-Authenticate": "Bearer"}
    # -- Verify Token --#
    try:
        payload = jwt.decode(token, JWT_REFRESH_KEY, algorithms=[JWT_ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired", headers=headers)
    except (JWTError, ValidationError) as ext:
        c.print(inspect(ext))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Token", headers=headers)
    return token_data
