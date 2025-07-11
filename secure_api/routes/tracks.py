from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Album, Artist, Track, Favorite, User
from secure_api.schemas.schemas import TrackExtended, TrackFull, TrackAll, TrackWithArtistAlbum
from sqlmodel import Session, select

tracks_router = APIRouter(dependencies=[Depends(get_currentUser)])


@tracks_router.get("/tracks", summary="Get array[] of all tracks", tags=["Track"],
                   response_model=List[TrackFull])
def get_tracks(*, db: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=8, le=10000)):
    tracks = db.exec(select(Track).offset(offset).limit(limit)).all()
    return tracks


@tracks_router.get("/tracks-albums-artists", summary="Get array[] of all tracks (with album and artist expanded)",
                   response_model=list[TrackAll], tags=["Track"])
def get_tracks_albums_artist(*, db: Session = Depends(get_session), me: User = Depends(get_currentUser),
               offset: int = 0, limit: int = Query(default=8, le=10000)):
    tracks = db.exec(select(Track).offset(offset).limit(limit)).all()
    favorites = db.exec(select(Favorite).where(Favorite.userID == me.userID)).all()

    for track in tracks:
        for fav in favorites:
            if (fav.trackID == track.trackID):
                track.isFavorite = True
    return tracks


@tracks_router.get("/track/{trackID}", summary="Get details of a single track",
                   response_model=TrackAll, tags=["Track"])
def get_track_trackID(*, db: Session = Depends(get_session), trackID: int):
    track = db.get(Track, trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track
