from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, Track, Album, Artist
from secure_api.schemas.schemas import TrackFull, CreateTrack, TrackExtended
from secure_api.auth.auth_api import get_currentUser


tracks_router = APIRouter(dependencies=[Depends(get_currentUser)])


@tracks_router.get("/tracks",
                   summary="Get array[] of all albums",
                   response_model=List[TrackFull], tags=["Track"])
def get_tracks(*, db: Session = Depends(get_session)):
    tracks = db.exec(select(Track).limit(8)).all()
    return tracks

@tracks_router.get("/track/{trackID}",
                   summary="Get details of a single track",
                   response_model=TrackExtended, tags=["Track"])
def get_track_trackID(*, db: Session = Depends(get_session), trackID: int):
    track = db.get(Track, trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    d_track = track.dict()
    artistID = d_track.pop("artistID")
    albumID = d_track.pop("albumID")
    artist = db.get(Artist, artistID)
    album = db.get(Album, albumID)

    db_track = TrackExtended(**track.dict())
    db_track.artist = artist
    db_track.album = album
    return db_track
