from pathlib import Path
from rich.traceback import install
install(show_locals=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from secure_api.database.database import create_db_and_tables
from secure_api.routes.auth import auth_router
from secure_api.routes.users import users_router
from secure_api.routes.playlists import playlists_router


app = FastAPI(
    debug=True,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # create_tracks()


music_path = Path.cwd().joinpath('secure_api', 'music')



origins = [
    "https://music-mvc13j.flutterflow.app",
    "https://complex.mangoboat.tv",
    "https://app.flutterflow.io",
    "http://localhost:8004",
]

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = ','.join(origins)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

app.add_middleware(CORSMiddleware,
                   allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)


app.include_router(auth_router, prefix="")
app.include_router(users_router, prefix="")
app.include_router(playlists_router, prefix="")


#if __name__ == '__main__':
#    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="debug")
