from fastapi import APIRouter, Depends, HTTPException, Query, status

from secure_api.auth.auth_api import get_currentUser

from secure_api.database.database import get_session
from secure_api.models.models import Track, Favorite, User
from secure_api.schemas.schemas import SearchTracks, TrackAll
from sqlmodel import Session, select, column


search_router = APIRouter(dependencies=[Depends(get_currentUser)])


@search_router.post("/search-tracks", summary="Search for Artists, Albums, and Tracks containing the query term",
                  response_model=list[TrackAll], tags=["Search"])
def search_tracks(*, data: SearchTracks, db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    tracks = db.exec(select(Track).filter(Track.trackURL.like("%"+data.term+"%"))).all()
    favorites = db.exec(select(Favorite).where(Favorite.userID == me.userID)).all()

    for track in tracks:
        for fav in favorites:
            if (fav.trackID == track.trackID):
                track.isFavorite = True
    return tracks
