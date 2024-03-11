from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from secure_api.database.database import create_db_and_tables
from secure_api.routes.auth import auth_router
from secure_api.routes.users import users_router
from secure_api.routes.playlists import playlists_router


app = FastAPI(debug=True)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # create_tracks()

music_path = Path.cwd().joinpath('secure_api', 'music')

app.mount(str(music_path), StaticFiles(directory=music_path), name="music")
app.include_router(auth_router, prefix="", tags=["Auth"])
app.include_router(users_router, prefix="", tags=["Users"])
app.include_router(playlists_router, prefix="", tags=["Playlists"])
