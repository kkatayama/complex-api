import secrets
from typing import List
from datetime import datetime, timedelta
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User
from secure_api.schemas.schemas import (
    CreateUser, LoginUser, EditUser, ChangePass, UserWithPlaylists, DeleteUser, TokenSchema, TokenPayload, RenewToken)
from secure_api.auth.auth_api import (
    get_currentUser, get_refreshUser, get_access_token, get_refresh_token, get_hashed_password,
    verify_password, create_access_token, create_refresh_token, reuseable_oauth)
from secure_api import configs


users_router = APIRouter(dependencies=[Depends(get_currentUser)])


@users_router.get("/users",
                  summary="Get array[] of all users",
                  response_model=List[User], tags=["User"])
def get_users(*, db: Session = Depends(get_session)):
    users = db.exec(select(User)).all()
    return users


@users_router.get("/user/{userID}",
                  summary="Get details of a single user",
                  response_model=UserWithPlaylists, tags=["User"])
def get_user_userID(*, db: Session = Depends(get_session), userID: int):
    user = db.exec(select(User).where(User.id == userID)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@users_router.patch("/user/{userID}",
                    summary="Edit a user's username",
                    response_model=User, tags=["User"])
def edit_user_userID(*, userID: int, user: EditUser, db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    db_user = db.get(User, userID)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if (userID != me.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your user")

    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@users_router.delete("/user/{userID}",
                     summary="Delete a user",
                     response_model=DeleteUser, tags=["User"])
def delete_user_userID(*, userID: int, db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    db_user = db.get(User, userID)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if (userID != me.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your user")

    db.delete(db_user)
    db.commit()
    return db_user
    return {"ok": True}
