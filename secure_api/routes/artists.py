from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, Album, Artist, Track
from secure_api.schemas.schemas import (
    ArtistFull, CreateArtist, ArtistWithAlbums, ArtistWithAlbumTracks)
from secure_api.auth.auth_api import get_currentUser


artists_router = APIRouter(dependencies=[Depends(get_currentUser)])


@artists_router.get("/artists",
                    summary="Get array[] of all artists",
                    response_model=List[ArtistFull], tags=["Artist"])
def get_artists(*, db: Session = Depends(get_session)):
    artists = db.exec(select(Artist)).all()
    return artists

@artists_router.get("/artist/{artistID}",
                    summary="Get details of a single artist",
                    response_model=ArtistWithAlbums, tags=["Artist"])
def get_artist_artistID(*, db: Session = Depends(get_session), artistID: int):
    artist = db.get(Artist, artistID)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    return artist

@artists_router.get("/artist/{artistID}/album/{albumID}",
                    summary="Get album details of a single artist",
                    response_model=ArtistWithAlbumTracks, tags=["Artist"])
def get_artist_artistID_album_albumID(*, db: Session = Depends(get_session), artistID: int, albumID: int):
    artist = db.get(Artist, artistID)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    album = db.get(Album, albumID)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    tracks = db.exec(select(Track).where(Track.artistID == artistID and Track.albumID == albumID)).all()

    db_artist = ArtistWithAlbumTracks(**artist.dict())
    db_artist.album = album
    db_artist.album.tracks = tracks
    return db_artist
