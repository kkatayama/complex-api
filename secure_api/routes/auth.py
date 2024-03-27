import secrets
from typing import Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm

from secure_api.database.database import get_session
from secure_api.models.models import User
from secure_api.schemas.schemas import (
    LoginUser, EditUser, UserBase, ChangePass, CreateUser, UserWithPlaylists, TokenSchema, TokenPayload, RenewToken)
from secure_api.auth.auth_api import (
    get_currentUser, get_refreshUser, get_accessToken, get_refreshToken, get_hashed_password,
    verify_password, create_accessToken, create_refreshToken, reuseable_oauth)
from secure_api import configs
from rich.console import Console


auth_router = APIRouter()

c = Console()

@auth_router.post("/sign-up", summary="Create a user account (via FORM)", response_model=User, tags=["Account-Security"])
def sign_up(*, username: str = Form(), password1: str = Form(), password2: str = Form(),
            db: Session = Depends(get_session), user: CreateUser):
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


@auth_router.post("/sign-in", summary="Submit credentials and retrieve access toens (via FORM)",
                  response_model=TokenSchema, tags=["Account-Security"])
def sign_in(*, username: str = Form(), password: str = Form(), db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    # -- Update User Status -- #
    user.loginStatus = True
    db.add(user)
    db.commit()
    db.refresh(user)

    accessExpires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refreshExpires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    accessToken = create_accessToken(user, accessExpires)
    refreshToken = create_refreshToken(user, refreshExpires)
    access_exp = get_accessToken(token=accessToken).exp
    refresh_exp = get_refreshToken(token=refreshToken).exp
    return TokenSchema(
        accessToken=accessToken, accessExpires=access_exp, refreshToken=refreshToken, refreshExpires=refresh_exp,
        userID=user.id, username=user.username, userRole=user.userRole, loginStatus=user.loginStatus)


#security = HTTPBearer()
# def refreshToken(*, user: User = Depends(get_refreshUser), authorization: Optional[str] = Depends(security)):
@auth_router.post('/refresh-token', summary="Refresh jwt API tokens (via FORM)",
                  response_model=TokenSchema, tags=["Account-Security"])
def refresh_token(*, token: str = Form(), db: Session = Depends(get_session)):
    # grant_type = username
    user = get_refreshUser(token=token)
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


@auth_router.get("/auth/me", summary='Get details of currently logged in user', response_model=User, tags=["Account-Security"])
def auth_me(*, user: User = Depends(get_currentUser)):
    return user

@auth_router.get("/auth/me/playlists", summary='Include user playlists', response_model=UserWithPlaylists, tags=["Account-Security"])
def auth_me_playlists(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.id == me.id)).first()
    return user

@auth_router.post('/test-access-token', summary="Test if the access token is valid", response_model=TokenPayload, tags=["Account-Security"])
def test_accessToken(*, data: TokenPayload = Depends(get_accessToken)):
    return data

@auth_router.post('/test-refresh-token', summary="Test if the refresh token is valid", response_model=TokenPayload, tags=["Account-Security"])
def test_refreshToken(*, form_data: OAuth2PasswordRequestForm = Depends()):
    grant_type = form_data.username
    data = get_refreshToken(token=form_data.password)
    return data

@auth_router.get("/logout", summary="Revoke all tokens and log the user out", tags=["Account-Security"])
def logout(*, c_user: User = Depends(get_currentUser), r_user: User = Depends(get_refreshUser),
           token: str = Depends(reuseable_oauth)):
    return dict(c_user=c_user, r_user=r_user, token=token)
