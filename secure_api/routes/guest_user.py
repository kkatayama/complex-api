import secrets
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from secure_api import configs
from secure_api.auth.auth_api import (create_access_token, get_currentUser,
                                      create_refresh_token, get_access_token,
                                      get_hashed_password, get_refresh_token,
                                      get_refreshUser, verify_password, reuseable_oauth)
from secure_api.database.database import get_session
from secure_api.models.models import User
from secure_api.schemas.schemas import (CreateUser, LoginUser, RenewToken,
                                        UserSignOut, TokenSchema)
from sqlmodel import Session, select
from pydantic import ValidationError

guest_router = APIRouter()


@guest_router.post("/create-user", summary="Create a user account (via JSON)",
                  response_model=User, tags=["User-Guest"])
def create_user(*, data: CreateUser, db: Session = Depends(get_session)):
    """
    Create a user account:

    - You can't sign-in if you don't have an account!
    """
    if not secrets.compare_digest(data.password1, data.password2):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    if db.exec(select(User).where(User.username == data.username)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exist")

    password = get_hashed_password(data.password1)
    user = User(userRole="Customer", username=data.username, password=password, loginStatus=False)
    db_user = User.model_validate(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@guest_router.post("/sign-in", summary="Submit credentials and retrieve access tokens (via JSON)",
                  response_model=TokenSchema, tags=["User-Guest"])
def sign_in(*, data: LoginUser, db: Session = Depends(get_session)):
    """
    Sign-in to the backend API:

    - **username**: your username
    - **password**: your password

    Returns:

    - **Token Details**: save the `access_token` to FlutterFlow to allow authenticated requests
    """
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

    access_expires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user, access_expires)
    refresh_token = create_refresh_token(user, refresh_expires)
    access_exp = get_access_token(token=access_token).exp
    refresh_exp = get_refresh_token(token=refresh_token).exp
    return TokenSchema(
        access_token=access_token, access_expires=access_exp, refresh_token=refresh_token, refresh_expires=refresh_exp,
        userID=user.userID, username=user.username, userRole=user.userRole, loginStatus=user.loginStatus)


@guest_router.get("/sign-out", summary="Sign out the currently logged in user",
                  response_model=UserSignOut, tags=["User-Guest"])
def sign_out(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
             request: Request):
    """
    Sign-out the currently logged in user.

    - **LoginStatus**: this will set the status to False.
    - **NOTE**: if you execute this endpoint in the [Interactive Documentation](https://api.mangoboat.tv/doc), you will need to refresh the page afterward in order to complete the sign-out process!
    """
    user = db.get(User, me.userID)

    user.loginStatus = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@guest_router.post("/renew-token", summary="Refresh jwt API tokens (via JSON)",
                   response_model=TokenSchema, tags=["User-Guest"], )
def renew_token(*, data: RenewToken, db: Session = Depends(get_session)):
    # grant_type = data.username
    user = get_refreshUser(token=data.access_token)
    if user is None:
        user.loginStatus = False
        db.add(user)
        db.commit()
        db.refresh(user)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to verify token, please login with username + password")
    access_expires = timedelta(configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires = timedelta(configs.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user, access_expires)
    refresh_token = create_refresh_token(user, refresh_expires)
    access_exp = get_access_token(token=access_token).exp
    refresh_exp = get_refresh_token(token=refresh_token).exp
    return TokenSchema(
        access_token=access_token, access_expires=access_exp, refresh_token=refresh_token, refresh_expires=refresh_exp,
        userID=user.userID, username=user.username, userRole=user.userRole, loginStatus=user.loginStatus)
