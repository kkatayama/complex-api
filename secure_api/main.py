from pathlib import Path
from rich.traceback import install
install(show_locals=True)

from fastapi import FastAPI

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

app.include_router(auth_router, prefix="")
app.include_router(users_router, prefix="")
app.include_router(playlists_router, prefix="")


#if __name__ == '__main__':
#    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="debug")
