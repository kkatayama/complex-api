# coding: utf-8
from datetime import timedelta
from sqlmodel import Session, select
from fastapi import FastAPI, APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm

from secure_api.database.database import get_session
from secure_api.models import models
from secure_api.auth import auth_api
from secure_api import configs

app = FastAPI()

@app.post('/')
def check(*, db: Session = Depends(get_session), data: models.UserEmail):
    return db.exec(select(models.User).where(models.User.email == data.email))
