from typing import Optional
from datetime import timedelta
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import secrets

from secure_api.database.database import get_session
from secure_api.models.models import User
from secure_api.schemas.schemas import (
    EditUser, ChangePass, CreateUser, UserWithPlaylists, TokenSchema, TokenPayload)
from secure_api.auth.auth_api import (
    get_current_user, get_refresh_user, get_access_token, get_refresh_token, get_hashed_password,
    verify_password, create_access_token, create_refresh_token, reuseable_oauth)
from secure_api import configs
from rich.console import Console


auth_router = APIRouter()

c = Console()


@auth_router.post("/sign-up", summary="Create a user account", response_model=User, tags=["User"])
def create_user(*, db: Session = Depends(get_session), user: CreateUser):
    if not secrets.compare_digest(user.password1, user.password2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    if db.exec(select(User).where(User.email == user.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")

    password = get_hashed_password(user.password1)
    db_user = User(name=user.name, email=user.email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@auth_router.post("/login", summary="Create access and refresh tokens for user", response_model=TokenSchema, tags=["JWT-OAuth2"])
def login(*, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    access_expires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    return TokenSchema(
        access_token=create_access_token(user.id, access_expires),
        refresh_token=create_refresh_token(user.id, refresh_expires))


#security = HTTPBearer()
@auth_router.post('/refresh', summary="Refresh jwt API tokens", response_model=TokenSchema, tags=["JWT-OAuth2"])
def refresh_token(*, form_data: OAuth2PasswordRequestForm = Depends()):
    grant_type = form_data.username
    user = get_refresh_uer(token=form_data.password)
# def refresh_token(*, user: User = Depends(get_refresh_user), authorization: Optional[str] = Depends(security)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Failed to verify token, please login with email + password")
    access_expires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    return TokenSchema(
        access_token=create_access_token(user.id, access_expires),
        refresh_token=create_refresh_token(user.id, refresh_expires))


@auth_router.get("/auth/me", summary='Get details of currently logged in user', response_model=User, tags=["JWT-OAuth2"])
def auth_me(*, user: User = Depends(get_current_user)):
    return user


@auth_router.get("/auth/me/playlists", summary='Include user playlists', response_model=UserWithPlaylists, tags=["JWT-OAuth2"])
def auth_me_playlists(*, user: User = Depends(get_current_user)):
    return user

@auth_router.post('/test-access-token', summary="Test if the access token is valid", response_model=TokenPayload, tags=["JWT-OAuth2"])
def test_access_token(*, data: TokenPayload = Depends(get_access_token)):
    return data

@auth_router.post('/test-refresh-token', summary="Test if the refresh token is valid", response_model=TokenPayload, tags=["JWT-OAuth2"])
def test_refresh_token(*, form_data: OAuth2PasswordRequestForm = Depends()):
    grant_type = form_data.username
    data = get_refresh_token(token=form_data.password)
    return data

@auth_router.get("/logout", summary="Revoke all tokens and log the user out", tags=["JWT-OAuth2"])
def logout(*, c_user: User = Depends(get_current_user), r_user: User = Depends(get_refresh_user),
           token: str = Depends(reuseable_oauth)):
    return dict(c_user = c_user, r_user = r_user, token = token)
