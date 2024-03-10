from fastapi import FastAPI

from secure_api.database.database import create_db_and_tables
from secure_api.routes.users import users_router
from secure_api.routes.playlists import playlists_router


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # create_tracks()


app.include_router(users_router, prefix="", tags=["Users"])
app.include_router(playlists_router)

