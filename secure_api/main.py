from pathlib import Path
import subprocess
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute

from secure_api.database.database import create_db_and_tables
from secure_api.database.init_db import insert_tracks

from secure_api.routes.auth import auth_router
from secure_api.routes.users import users_router
from secure_api.routes.artists import artists_router
from secure_api.routes.albums import albums_router
from secure_api.routes.tracks import tracks_router
from secure_api.routes.playlists import playlists_router
from secure_api.routes.guest_user import guest_router

from fastapi_middleware_logger.fastapi_middleware_logger import add_custom_logger
import logging
from rich.logging import RichHandler


logging.basicConfig(level="DEBUG", format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])


app = FastAPI(debug=True, openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")
app = add_custom_logger(app)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    insert_tracks()
    #p = subprocess.run(f'{sys.executable} -m secure_api.database.init_db', shell=True, text=True)


# music_path = Path.cwd().joinpath('secure_api', 'music')
origins = [
    "https://music-mvc13j.flutterflow.app",
    "https://complex.mangoboat.tv",
    "https://api.mangoboat.tv",
    "https://app.flutterflow.io",
    "http://localhost:8004"
]


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = ','.join(origins)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


# -- Enable CORS - Trusted Origins
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# -- API Routes: auth, users, playlists, tracks, artists, albums
app.include_router(auth_router, prefix="")
app.include_router(guest_router, prefix="")
app.include_router(users_router, prefix="")
app.include_router(artists_router, prefix="")
app.include_router(albums_router, prefix="")
app.include_router(tracks_router, prefix="")
app.include_router(playlists_router, prefix="")

# -- Music Paths: "/music/Netsky/Second Nature/01 - Hold On (feat. Becky Hill).mp3"
app.mount("/music", StaticFiles(directory="secure_api/music"), name="music")

# -- "read_users_users_get" => "read_users"
def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'

use_route_names_as_operation_ids(app)

#if __name__ == '__main__':
#    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="debug")
