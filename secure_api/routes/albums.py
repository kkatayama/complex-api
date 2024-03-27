from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, Album
from secure_api.schemas.schemas import AlbumFull, AlbumWithArtistTracks
from secure_api.auth.auth_api import get_currentUser


albums_router = APIRouter(dependencies=[Depends(get_currentUser)])


@albums_router.get("/albums/", response_model=List[AlbumFull], tags=["Album"])
def read_albums(*, db: Session = Depends(get_session)):
    albums = db.exec(select(Album)).all()
    return albums

@albums_router.get("/albums/{albumID}", response_model=AlbumWithArtistTracks, tags=["Album"])
def read_album(*, db: Session = Depends(get_session), albumID: int):
    album = db.get(Album, albumID)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return album

@albums_router.get("/albums/{albumID}/tracks", response_model=AlbumWithArtistTracks, tags=["Album"])
def read_album_tracks(*, db: Session = Depends(get_session), albumID: int):
    album = db.get(Album, albumID)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return album
