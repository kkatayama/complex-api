from pathlib import Path
import subprocess
import sys

from rich import inspect

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from fastapi.responses import HTMLResponse
from fastapi_pagination import add_pagination
from apitally.fastapi import ApitallyMiddleware


from secure_api.database.database import create_db_and_tables, get_session
from secure_api.database.init_db import insert_tracks
from secure_api.templates.redoc import get_redoc_html
from secure_api.templates.desc import description

from secure_api.routes.guest_user import guest_router
from secure_api.routes.my import my_router
from secure_api.routes.users import users_router
from secure_api.routes.artists import artists_router
from secure_api.routes.albums import albums_router
from secure_api.routes.tracks import tracks_router
from secure_api.routes.search import search_router
from secure_api.routes.playlists import playlists_router
from secure_api.routes.playhistory import playhistory_router
from secure_api.routes.favorites import favorites_router
from secure_api.routes.image import images_router
from secure_api.routes.auth import auth_router
from secure_api.routes.suggested import suggested_router
from secure_api.routes.tables import tables_router
from secure_api.routes.media import media_router
from secure_api.routes.palette import palette_router

from secure_api.middlewares.exception import ExceptionHandlerMiddleware


###############################################################################
#                                    Sentry                                   #
###############################################################################
# import sentry_sdk
#
# sentry_sdk.init(
#     dsn="https://62dc00db2bea9fbfba2e378c3bc68514@o4506715665137664.ingest.us.sentry.io/4507057420894208",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     traces_sample_rate=1.0,
#     # Set profiles_sample_rate to 1.0 to profile 100%
#     # of sampled transactions.
#     # We recommend adjusting this value in production.
#     profiles_sample_rate=1.0,
#     enable_tracing=True,
# )




# from fastapi_middleware_logger.fastapi_middleware_logger import add_custom_logger

# import logging
# from rich.logging import RichHandler
# logging.basicConfig(level="DEBUG", format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])


#app = FastAPI(debug=True, openapi_url="/openapi.json", docs_url="/docs", redoc_url="/redoc")
#app = add_custom_logger(app)
app = FastAPI(debug=True, openapi_url="/openapi.json", docs_url="/docs", redoc_url=None,
              title="Com-Plex Backend API", description=description, version="0.9.1",
              license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
              servers=[
                  {"url": "https://api.mangoboat.tv", "description": "Backend environment"},
              ],
              swagger_ui_parameters = {"docExpansion":"none"},
)


###############################################################################
#                                   Apitally                                  #
###############################################################################
# app.add_middleware(
#     ApitallyMiddleware,
#     client_id="87206744-08dd-43ae-841e-a254df5c2ac0",
#     env="prod",
# )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    insert_tracks()
    #p = subprocess.run(f'{sys.executable} -m secure_api.database.init_db', shell=True, text=True)


# music_path = Path.cwd().joinpath('secure_api', 'music')

origins = [
    "https://com-plex-lmp029.flutterflow.app/",
    "https://music-mvc13j.flutterflow.app",
    "https://complex.mangoboat.tv",
    "https://api.mangoboat.tv",
    "https://app.flutterflow.io",
    "http://localhost",
    "http://localhost:8004",
    "http://192.168.1.37:8004",
    "*"
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

# -- Enable Better Error Reporting?
# -- https://python.plainenglish.io/effortless-exception-error-handling-in-fastapi-a-clean-and-simplified-approach-db6f6a7a497c
app.add_middleware(ExceptionHandlerMiddleware)

# https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body, }),
#     )


# -- API Routes: auth, users, playlists, tracks, artists, albums
app.include_router(guest_router, prefix="")
app.include_router(my_router, prefix="")
app.include_router(users_router, prefix="")
app.include_router(artists_router, prefix="")
app.include_router(albums_router, prefix="")
app.include_router(tracks_router, prefix="")
app.include_router(search_router, prefix="")
app.include_router(playlists_router, prefix="")
app.include_router(playhistory_router, prefix="")
app.include_router(favorites_router, prefix="")
app.include_router(images_router, prefix="")
app.include_router(suggested_router, prefix="")
app.include_router(tables_router, prefix="")
app.include_router(auth_router, prefix="")
app.include_router(media_router, prefix="")
app.include_router(palette_router, prefix="")

add_pagination(app)

# -- Music Paths: "/music/Netsky/Second Nature/01 - Hold On (feat. Becky Hill).mp3"
#app.mount("/music", StaticFiles(directory="secure_api/music"), name="music")

# # -- DataTables Path
# app.mount("/DataTables", StaticFiles(directory="secure_api/DataTables"), name="DataTables")

# app.mount("/css", StaticFiles(directory="secure_api/css"), name="css")

@app.get("/redoc", include_in_schema=False)
def redoc_try_it_out() -> HTMLResponse:
    # app.openapi_version = "3.0.0"
    title = app.title + " Redoc with try it out"
    return get_redoc_html(openapi_url=app.openapi_url, title=title)


# Running at FinTech!


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



# if __name__ == '__main__':
    # uvicorn.run(app, host="0.0.0.0", port=8004, log_level="debug")
