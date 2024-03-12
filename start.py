from pathlib import Path
from rich.traceback import install
install(show_locals=True)

from uvicorn.logging import logging
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware import Middleware
from asgi_logger import AccessLoggerMiddleware

from secure_api.database.database import create_db_and_tables
from secure_api.routes.auth import auth_router
from secure_api.routes.users import users_router
from secure_api.routes.playlists import playlists_router

# -- erase uvicorn handlers for logger
# https://github.com/Kludex/asgi-logger/tree/main?tab=readme-ov-file#usage
logging.getLogger("uvicorn.access").handlers = []


app = FastAPI(middleware=[Middleware(AccessLoggerMiddleware)])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # create_tracks()

app.include_router(auth_router, prefix="", tags=["Auth"])
app.include_router(users_router, prefix="", tags=["Users"])
app.include_router(playlists_router, prefix="", tags=["Playlists"])

music_path = Path.cwd().joinpath('secure_api', 'music')
staticfiles = StaticFiles(directory=str(music_path))
app.mount("/static", staticfiles, name="static")



if __name__ == '__main__':
    create_db_and_tables()
    uvicorn.run("start:app", host="0.0.0.0", port=8002, reload=True)
