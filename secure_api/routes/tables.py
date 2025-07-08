import pandas as pd

from fastapi import FastAPI, Request, APIRouter, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# from fastapi_pagination import Page
# from fastapi_pagination.ext.sqlmodel import paginate

from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session, engine
from secure_api.models.models import (User, Artist, Album, Track, Image, Playlist, PlaylistTrack,
                                      PlayHistory, Favorite, SuggestedArtist, SuggestedAlbum)
from sqlmodel import Session, select

import re


# -- helper function to return Pandas generated HTML Table when expected in request...
def genTable(records, caption, count=0):
    table_id = f'table-{count}'
    styles = [dict(selector="caption", props=[("text-align", "center"), ("font-size", "150%"), ("color", 'black')])]
    df = pd.DataFrame(records)
    s = df.style.set_caption(caption).set_table_styles(styles)
    table = s.to_html()
    html = re.sub(r'( id="(T_[_a-z0-9]+)"| class="([_a-z0-9 ]+)" |<style.*</style>\n)', '', table, flags=re.DOTALL)
    html = re.sub(r'(https://api.mangoboat.tv/music/.+(poster|cover).jpg)', r'<img src="\1" height="100"></img>', html)
    html = re.sub(r'(https://api.mangoboat.tv/music/.+\.mp3)', r'<audio controls src="\1"></audio>', html)
    html = html.replace('<th>&nbsp;</th>', '<th>index</th>')
    # html = html.replace('<table>', f'<table id="{table_id}" class="dataTable display compact hover" style="width:100%">')
    html = html.replace('<table>', f'<table id="{table_id}" class="display compact hover" style="width:100%">')
    # html = html.replace('<caption>', '<caption class="mytable caption">')
    # with open(table_id+'.html', 'w') as f:
    #     f.write(html)
    thead = re.search(r'(\s+<thead>.+</thead>)', html, flags=re.DOTALL).group()
    # tfoot = thead.replace('thead', 'tfoot')
    # html = html.replace('</tbody>', f'</tbody>{tfoot}')

    # html = html.replace('<thead>', '<thead class="table-dark">')
    # html = html.replace('<tbody>', '<tbody class="table-group-divider">')
    html = html.replace('<caption>', '<caption style="color: blue; font-size: 1.4em; font-weight: bold; border: 2px solid powderblue;">')
    return html

templates = Jinja2Templates(directory="secure_api/templates")


# include_in_schema=False,
tables_router = APIRouter(tags=["Tables"])



@tables_router.get('/tables', response_class=HTMLResponse, include_in_schema=False)
def get_tables(request: Request, db: Session = Depends(get_session)):
    tables = {}
    for i, table in enumerate(["User", "Playlist", "PlaylistTrack", "PlayHistory"]): #, "Artist","Album", "Track", "Image"]):
        db_table = db.exec(select(eval(table))).all()
        #df_table = pd.DataFrame([item.model_dump() for item in db_table])
        html_table = genTable([item.model_dump() for item in db_table], f"Table: {table}", count=i)
        tables.update({f'table_{i}': html_table})
        #print(html_table)
    context = {'request': request, "title": "Com-Plex API Database Tables", **tables}
    # return templates.TemplateResponse("tables.html", context)
    return templates.TemplateResponse("tables2.html", context)


@tables_router.get('/table-users', summary="Users Table", response_model=list[User])
def get_table_users(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(User).offset(offset).limit(limit)).all()

@tables_router.get('/table-favorites', summary="Favorites Table", response_model=list[Favorite])
def get_table_favorites(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(Favorite).offset(offset).limit(limit)).all()

@tables_router.get('/table-playlists', summary="Playlists Table", response_model=list[Playlist])
def get_table_playlists(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(Playlist).offset(offset).limit(limit)).all()

@tables_router.get('/table-playlist-tracks', summary="Playlist Tracks Table", response_model=list[PlaylistTrack])
def get_table_playlist_tracks(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(PlaylistTrack).offset(offset).limit(limit)).all()

@tables_router.get('/table-play-history', summary="PlayHistory Table", response_model=list[PlayHistory])
def get_table_play_history(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(PlayHistory).offset(offset).limit(limit)).all()

@tables_router.get("/table-artists", summary="Artists Table", response_model=list[Artist])
def get_table_artists(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                     offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(Artist).offset(offset).limit(limit)).all()

@tables_router.get('/table-albums', summary="Albums Table", response_model=list[Album])
def get_table_albums(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(Album).offset(offset).limit(limit)).all()

@tables_router.get('/table-tracks', summary="Tracks Table", response_model=list[Track])
def get_table_tracks(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=10000)):
    return db.exec(select(Track).offset(offset).limit(limit)).all()

@tables_router.get('/table-images', summary="Images Table", response_model=list[Image])
def get_table_images(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(Image).offset(offset).limit(limit)).all()

@tables_router.get('/table-suggested-artists', summary="Suggested Artists Table", response_model=list[SuggestedArtist])
def get_table_suggested_artists(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(SuggestedArtist).offset(offset).limit(limit)).all()

@tables_router.get('/table-suggested-albums', summary="Suggested Albums Table", response_model=list[SuggestedAlbum])
def get_table_suggested_albums(db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    offset: int = 0, limit: int = Query(default=8, le=1000)):
    return db.exec(select(SuggestedAlbum).offset(offset).limit(limit)).all()
