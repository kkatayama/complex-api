import secrets
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from rich.console import Console
from secure_api import configs
from secure_api.auth.auth_api import (create_access_token,
                                      create_refresh_token, get_access_token,
                                      get_currentUser, get_hashed_password,
                                      get_refresh_token, get_refreshUser,
                                      reuseable_oauth, verify_password)
from secure_api.database.database import get_session
from secure_api.models.models import User
from secure_api.schemas.schemas import (CreateUser, TokenPayload, TokenSchema,
                                        UserWithPlaylists)
from sqlmodel import Session, select

auth_router = APIRouter()

c = Console()

@auth_router.post("/sign-up", summary="Create a user account (via FORM)", response_model=User, tags=["Account-Security"])
def sign_up(*, db: Session = Depends(get_session), user: CreateUser):
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


@auth_router.post("/login", summary="Submit credentials and retrieve access tokens (via FORM)",
                  response_model=TokenSchema, tags=["Account-Security"])
# def login(*, username: str = Form(), password: str = Form(), db: Session = Depends(get_session)):
def login(*, form_data: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.username == form_data.username)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username: already exists!")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    # # -- Update User Status -- #
    user.loginStatus = True
    db.add(user)
    db.commit()
    db.refresh(user)

    access_expires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user, access_expires)
    refresh_token = create_refresh_token(user, refresh_expires)
    access_exp = get_access_token(token=access_token).exp
    refresh_exp = get_refresh_token(token=refresh_token).exp
    return TokenSchema(
        access_token=access_token, access_expires=access_exp,
        refresh_token=refresh_token, refresh_expires=refresh_exp,
        userID=user.userID, username=user.username,
        userRole=user.userRole, loginStatus=user.loginStatus)


#security = HTTPBearer()
# def refresh_token(*, user: User = Depends(get_refreshUser), authorization: Optional[str] = Depends(security)):
@auth_router.post("/refresh-token", summary="Refresh jwt API tokens (via FORM)",
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
    access_expires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user, access_expires)
    refresh_token = create_refresh_token(user, refresh_expires)
    access_exp = get_access_token(token=access_token).exp
    refresh_exp = get_refresh_token(token=refresh_token).exp
    return TokenSchema(
        access_token=access_token, access_expires=access_exp, refresh_token=refresh_token, refresh_expires=refresh_exp,
        userID=user.userID, username=user.username, userRole=user.userRole, loginStatus=user.loginStatus)


@auth_router.get("/auth/me", summary="Get details of currently logged in user", response_model=User, tags=["Account-Security"])
def auth_me(*, user: User = Depends(get_currentUser)):
    return user

@auth_router.get("/auth/me/playlists", summary="Include user playlists", response_model=UserWithPlaylists, tags=["Account-Security"])
def auth_me_playlists(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.userID == me.userID)).first()
    return user

@auth_router.post("/test-access-token", summary="Test if the access token is valid", response_model=TokenPayload, tags=["Account-Security"])
def test_access_token(*, data: TokenPayload = Depends(get_access_token)):
    return data

@auth_router.post("/test-refresh-token", summary="Test if the refresh token is valid", response_model=TokenPayload, tags=["Account-Security"])
def test_refresh_token(*, form_data: OAuth2PasswordRequestForm = Depends()):
    grant_type = form_data.username
    data = get_refresh_token(token=form_data.password)
    return data

@auth_router.get("/logout", summary="Revoke all tokens and log the user out", tags=["Account-Security"])
def logout(*, c_user: User = Depends(get_currentUser), r_user: User = Depends(get_refreshUser),
           token: str = Depends(reuseable_oauth)):
    return dict(c_user=c_user, r_user=r_user, token=token)
