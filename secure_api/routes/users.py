import secrets
from typing import List
from datetime import datetime, timedelta
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User
from secure_api.schemas.schemas import (
    CreateUser, LoginUser, EditUser, ChangePass, UserWithPlaylists, TokenSchema, TokenPayload, RenewToken)
from secure_api.auth.auth_api import (
    get_currentUser, get_refreshUser, get_access_token, get_refresh_token, get_hashed_password,
    verify_password, create_access_token, create_refresh_token, reuseable_oauth)
from secure_api import configs


users_router = APIRouter(dependencies=[Depends(get_currentUser)])


@users_router.get("/users", summary="Get array[] of all users", response_model=List[User], tags=["User"])
def read_users(*, db: Session = Depends(get_session)):
    users = db.exec(select(User)).all()
    return users


@users_router.get("/users/{userID}", summary="Get details of a user", response_model=UserWithPlaylists, tags=["User"])
def read_user(*, db: Session = Depends(get_session), userID: int):
    user = db.exec(select(User).where(User.id == userID)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@users_router.patch("/users/{userID}", summary="Edit user details", tags=["User"])
def edit_user(*, userID: int, user: EditUser, db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
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


@users_router.patch("/change-password", summary="Change password", tags=["User"])
def change_password(*, user: ChangePass, db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    if not verify_password(user.old_password, me.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    hashed_password = get_hashed_password(user.new_password)
    me.password = hashed_password
    db.add(me)
    db.commit()
    db.refresh(me)
    return me


@users_router.delete("/users/{userID}", summary="Delete user", tags=["User"])
def delete_user(*, userID: int, db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    db_user = db.get(User, userID)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if (userID != me.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your user")

    db.delete(db_user)
    db.commit()
    return {"ok": True}
