import secrets
from typing import Annotated
from datetime import datetime, timedelta
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User
from secure_api.schemas.schemas import (
    CreateUser, LoginUser, EditUser, ChangePass, UserWithPlaylists, TokenSchema, TokenPayload, RenewToken)
from secure_api.auth.auth_api import (
    get_currentUser, get_refreshUser, get_accessToken, get_refreshToken, get_hashed_password,
    verify_password, create_accessToken, create_refreshToken, reuseable_oauth)
from secure_api import configs


guest_router = APIRouter()


@guest_router.post("/login", summary="Submit credentials and retrieve access toens (via JSON)",
                  response_model=TokenSchema, tags=["User-Guest"])
def login(*, data: LoginUser, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.username == data.username)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    # -- Update User Status -- #
    user.loginStatus = True
    db.add(user)
    db.commit();
    db.refresh(user)

    accessExpires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refreshExpires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    accessToken=create_accessToken(user, accessExpires)
    refreshToken=create_refreshToken(user, refreshExpires)
    access_exp = get_accessToken(token=accessToken).exp
    refresh_exp = get_refreshToken(token=refreshToken).exp
    return TokenSchema(
        accessToken=accessToken, accessExpires=access_exp, refreshToken=refreshToken, refreshExpires=refresh_exp,
        userID=user.id, username=user.username, userRole=user.userRole, loginStatus=user.loginStatus)


#security = HTTPBearer()
# def refreshToken(*, user: User = Depends(get_refreshUser), authorization: Optional[str] = Depends(security)):
@guest_router.post('/renew-token', summary="Refresh jwt API tokens (via JSON)",
                  response_model=TokenSchema, tags=["User-Guest"])
def renew_token(*, data: RenewToken, db: Session = Depends(get_session)):
    # grant_type = data.username
    user = get_refreshUser(token=data.password)
    if user is None:
        user.loginStatus = False
        db.add(user)
        db.commit()
        db.refresh(user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Failed to verify token, please login with username + password")
    accessExpires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refreshExpires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    accessToken = create_accessToken(user, accessExpires)
    refreshToken = create_refreshToken(user, refreshExpires)
    access_exp = get_accessToken(token=accessToken).exp
    refresh_exp = get_refreshToken(token=refreshToken).exp
    return TokenSchema(
        accessToken=accessToken, accessExpires=access_exp, refreshToken=refreshToken, refreshExpires=refresh_exp,
        userID=user.id, username=user.username, userRole=user.userRole, loginStatus=user.loginStatus)


@guest_router.post("/create-user", summary="Create a user account (via JSON)",
                  response_model=User, tags=["User-Guest"])
def create_user(*, user: CreateUser, db: Session = Depends(get_session)):
    if not secrets.compare_digest(user.password1, user.password2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    if db.exec(select(User).where(User.username == user.username)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exist")

    password = get_hashed_password(user.password1)
    db_user = User(userRole="Customer", username=user.username, password=password, loginStatus=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
