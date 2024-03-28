from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, Track, Album, Artist
from secure_api.schemas.schemas import TrackFull, CreateTrack, TrackWithAlbumArtist
from secure_api.auth.auth_api import get_currentUser


tracks_router = APIRouter(dependencies=[Depends(get_currentUser)])


@tracks_router.get("/tracks/", tags=["Track"])
def read_tracks(*, db: Session = Depends(get_session)):
    tracks = db.exec(select(Track).limit(2)).all()
    return tracks

@tracks_router.get("/tracks/{trackID}",  tags=["Track"])
def read_track(*, db: Session = Depends(get_session), trackID: int):
    track = db.get(Track, trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    artistID = track.artistID
    albumID = track.albumID
    artist = db.get(Artist, artistID)
    album = db.get(Album, albumID)

    db_track = track.dict()
    db_track["album"] = album.dict()
    db_track["artist"] = artist.dict()
    return db_track
