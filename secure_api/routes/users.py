from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, UserOut, UserWithPlaylists  # , UserUpdate
from secure_api.auth.auth_api import get_current_user


users_router = APIRouter(dependencies=[Depends(get_current_user)])


@users_router.get("/users/", summary="Get array[] of all users", response_model=List[UserOut])
def read_users(*, db: Session = Depends(get_session)):
    users = db.exec(select(User)).all()
    return users


@users_router.get("/users/{user_id}", summary="Get details of a user", response_model=UserWithPlaylists)
def read_user(*, db: Session = Depends(get_session) , user_id: int):
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
