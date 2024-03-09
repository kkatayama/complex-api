from sqlmodel import Session, create_engine

from secure_api import configs
from secure_api.models import models


sqlite_url = f'sqlite:///./{configs.DB_FILE}'
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
