from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, Track
from secure_api.schemas.schemas import TrackFull, CreateTrack, TrackWithAlbumArtist
from secure_api.auth.auth_api import get_currentUser


tracks_router = APIRouter(dependencies=[Depends(get_currentUser)])


@tracks_router.get("/tracks/", response_model=List[TrackFull], tags=["Track"])
def read_tracks(*, db: Session = Depends(get_session)):
    tracks = db.exec(select(Track)).all()
    return tracks

@tracks_router.get("/tracks/{trackID}", response_model=TrackWithAlbumArtist, tags=["Track"])
def read_track(*, db: Session = Depends(get_session), trackID: int):
    track = db.get(Track, trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track

@tracks_router.get("/tracks/{trackID}/tracks", response_model=TrackWithAlbumArtist, tags=["Track"])
def read_track_tracks(*, db: Session = Depends(get_session), trackID: int):
    track = db.get(Track, trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track
