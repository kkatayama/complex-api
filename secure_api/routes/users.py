from datetime import datetime, timedelta

from typing import List
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

users_router = APIRouter()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(session: Session, username: str):
    return session.exec(select(models.User).where(models.User.username == username)).first()


@users_router.post("/users/", response_model=models.UserRead)
def create_user(*, session: Session = Depends(get_session), user: models.UserCreate):
    print(f'\nuser = {user}')
    temp_user = get_user(session, user.username)
    print(f'temp_user = {temp_user}\n')
    db_user = models.User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@users_router.get("/users/", response_model=List[models.UserRead])
def read_users(*, session: Session = Depends(get_session)):
    users = session.exec(select(models.User)).all()
    print(f'\nusers = {users}\n')
    return users


@users_router.get("/users/{user_id}", response_model=models.UserWithPlaylists)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(models.User, user_id)
    print(f'\nuser = {user}\n')
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
