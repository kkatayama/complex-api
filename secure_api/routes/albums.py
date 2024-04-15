from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Album
from secure_api.schemas.schemas import AlbumFull, AlbumAll, AlbumWithTracks
from sqlmodel import Session, select


albums_router = APIRouter(dependencies=[Depends(get_currentUser)])


@albums_router.get("/albums", summary="Get array[] of all albums",
                   response_model=List[AlbumFull], tags=["Album"])
def get_albums(*, db: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=8, le=1000)):
    albums = db.exec(select(Album).offset(offset).limit(limit)).all()
    return albums

@albums_router.get("/albums-artists", summary="Get array[] of all albums (with artists expanded)",
                   response_model=List[AlbumAll], tags=["Album"])
def get_albums_artists(*, db: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=8, le=1000)):
    albums = db.exec(select(Album).offset(offset).limit(limit)).all()
    return albums


@albums_router.get("/album/{albumID}/tracks", summary="Get info for a single album (with tracks)", tags=["Album"],
                   response_model=AlbumWithTracks)
def get_album_albumID(*, db: Session = Depends(get_session),
                      albumID: int):
    album = db.get(Album, albumID)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bad albumID, no Album has (albumID={albumID})")
    return album
