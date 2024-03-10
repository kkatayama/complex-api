from datetime import timedelta
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from secure_api.database.database import get_session
from secure_api.models import models
from secure_api.auth import auth_api
from secure_api import configs


auth_router = APIRouter()


@auth_router.post("/login", summary="Create access and refresh tokens for user", response_model=models.TokenSchema)
def login(*, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.exec(select(models.User).where(models.User.email == form_data.username)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email")
    if not auth_api.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    return models.TokenSchema(
        access_token=auth_api.create_access_token(user.email),
        refresh_token=auth_api.create_refresh_token(user.email))

@auth_router.get("/auth/me", response_model=models.User)
def read_auth_me(*, current_user: models.User = Depends(auth_api.get_current_user)):
    return current_user


@auth_router.get("/auth/me/playlists", response_model=models.UserWithPlaylists)
def read_auth_me_playlists(*, current_user: models.User = Depends(auth_api.get_current_active_user)):
    return current_user
