from datetime import timedelta
from sqlmodel import Session
from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from secure_api.database.database import get_session
from secure_api.models import models
from secure_api.auth import auth_api
from secure_api import configs


auth_router = APIRouter()


@auth_router.post("/auth/login", response_model=models.Token)
def login(*, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = auth_api.authenticate_user(db, form.username, form.password)
    expires = timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_api.create_access_token(data={"sub": user.email}, expires_delta=expires)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/auth/me", response_model=models.UserRead)
def read_auth_me(*, current_user: models.User = Depends(auth_api.get_current_active_user)):
    return current_user


@auth_router.get("/auth/me/playlists", response_model=models.UserWithPlaylists)
def read_auth_me_playlists(*, current_user: models.User = Depends(auth_api.get_current_active_user)):
    return current_user
