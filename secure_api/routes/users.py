import secrets

from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_409_CONFLICT

from secure_api.database.database import get_session
from secure_api.models import models
from secure_api.auth import auth_api


users_router = APIRouter()


@users_router.post("/signup", response_model=models.User)
def create_user(*, db: Session = Depends(get_session), user: models.UserCreate):
    db_user = models.User.model_validate(user)
    user = db.exec(select(models.User).where(models.User.email == db_user.email)).first()
    if user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")


    if not secrets.compare_digest(user.password1.encode(), user.password2.encode()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords don't math")
    if auth_api.get_user(db, user.email):
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="E-mail already exists")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@users_router.get("/users/", response_model=List[models.User])
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
