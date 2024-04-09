from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Album, Artist, Track
from secure_api.schemas.schemas import TrackExtended, TrackFull, TrackAll, TrackWithArtistAlbum
from sqlmodel import Session, select

tracks_router = APIRouter(dependencies=[Depends(get_currentUser)])


@tracks_router.get("/tracks", summary="Get array[] of all albums", tags=["Track"],
                   response_model=List[TrackFull])
def get_tracks(*, db: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=8, le=1000)):
    tracks = db.exec(select(Track).offset(offset).limit(limit)).all()
    return tracks

@tracks_router.get("/track/{trackID}", summary="Get details of a single track",
                   response_model=TrackAll, tags=["Track"])
def get_track_trackID(*, db: Session = Depends(get_session), trackID: int):
    track = db.get(Track, trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track
