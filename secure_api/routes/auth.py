from datetime import timedelta
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import secrets

from secure_api.database.database import get_session
from secure_api.models.models import (
    User, UserUpdate, UserUpdatePass, UserCreate, UserWithPlaylists, TokenSchema)
from secure_api.auth.auth_api import (
    get_current_user, get_refresh_user, get_hashed_password, verify_password,
    create_access_token, create_refresh_token, reuseable_oauth)
from secure_api import configs


auth_router = APIRouter()


@auth_router.post("/sign-up", summary="Create a user account", response_model=UserUpdate)
def create_user(*, db: Session = Depends(get_session), user: UserCreate):
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


@auth_router.post("/login", summary="Create access and refresh tokens for user", response_model=TokenSchema)
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

@auth_router.post("/change-password", summary="Change password")
def change_password(*, user: UserUpdatePass, db: Session = Depends(get_session), me: User = Depends(get_current_user)):
    if not verify_password(user.old_password, me.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    hashed_password = get_hashed_password(user.new_password)
    me.password = hashed_password
    db.add(me)
    db.commit()
    db.refresh(me)
    return me

@auth_router.post('/refresh', summary="Refresh jwt API tokens", response_model=TokenSchema)
def refresh_token(*, user: User = Depends(get_refresh_user)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Failed to verify token, please login with email + password")
    access_expires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    return TokenSchema(
        access_token=create_access_token(user.id, access_expires),
        refresh_token=create_refresh_token(user.id, refresh_expires))


@auth_router.get("/auth/me", summary='Get details of currently logged in user', response_model=User)
def auth_me(*, user: User = Depends(get_current_user)):
    return user


@auth_router.get("/auth/me/playlists", summary='Include user playlists', response_model=UserWithPlaylists)
def auth_me_playlists(*, user: User = Depends(get_current_user)):
    return user


@auth_router.post('/test-token', summary="Test if the access token is valid", response_model=User)
def test_token(*, user: User = Depends(get_current_user)):
    return user


@auth_router.get("/logout", summary="Revoke all tokens and log the user out")
def logout(*, c_user: User = Depends(get_current_user), r_user: User = Depends(get_refresh_user),
           token: str = Depends(reuseable_oauth)):
    return dict(c_user = c_user, r_user = r_user, token = token)
