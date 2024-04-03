from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Album, Artist, Track
from secure_api.schemas.schemas import (ArtistFull, ArtistWithAlbums, AlbumAll,
                                        ArtistWithAlbumTracks, ArtistWithAlbumsTracks)
from sqlmodel import Session, select


artists_router = APIRouter(dependencies=[Depends(get_currentUser)])


@artists_router.get("/artists", summary="Get array[] of all artists", tags=["Artist"],
                    response_model=List[ArtistFull])
def get_artists(*, db: Session = Depends(get_session),
                offset: int = 0, limit: int = Query(default=8, le=1000)):
    artists = db.exec(select(Artist).offset(offset).limit(limit)).all()
    return artists


@artists_router.get("/artist/{artistID}/albums", summary="Get info for a single artist (includes albums)", tags=["Artist"],
                    response_model=ArtistWithAlbums)
def get_artist_artistID_albums(*, db: Session = Depends(get_session),
                               artistID: int):
    artist = db.get(Artist, artistID)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bad artistID, no Artist has (artistID={artistID})")
    return artist


@artists_router.get("/artist/{artistID}/album/{albumID}/tracks", summary="Get a single artist's album (with tracks)", tags=["Artist"],
                    response_model=ArtistWithAlbumTracks)
def get_artist_artistID_album_albumID_tracks(*, db: Session = Depends(get_session),
                                             artistID: int, albumID: int):
    artist = db.get(Artist, artistID)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bad artistID, no Artist has (artistID={artistID})")
    album = db.get(Album, albumID)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bad albumID, no Album has (albumID={albumID})")
    if (album.artistID != artistID):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Bad albumID, Artist does not have an Album with (albumID={albumID})")
    return ArtistWithAlbumTracks(**artist.dict(), album=album)


@artists_router.get("/artist/{artistID}/albums-tracks", summary="Get all albums with tracks for a single artist", tags=["Artist"],
                    response_model=ArtistWithAlbumsTracks)
def get_artist_artistID_albums_tracks(*, db: Session = Depends(get_session),
                               artistID: int):
    artist = db.get(Artist, artistID)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bad artistID, no Artist has (artistID={artistID})")
    return artist
