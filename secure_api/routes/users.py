from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException

from secure_api.database.database import get_session
from secure_api.models import models


users_router = APIRouter()


@users_router.post("/users/", response_model=models.UserRead)
def create_user(*, session: Session = Depends(get_session), user: models.UserCreate):
    print(f'\nuser = {user}\n')
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
