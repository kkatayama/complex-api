from fastapi import APIRouter, Depends, HTTPException, Query, status

from secure_api.auth.auth_api import get_currentUser

from secure_api.database.database import get_session
from secure_api.models.models import Track
from secure_api.schemas.schemas import SearchTracks, TrackAll
from sqlmodel import Session, select, column


search_router = APIRouter(dependencies=[Depends(get_currentUser)])


@search_router.post("/search-tracks", summary="Search for Artists, Albums, and Tracks containing the query term",
                  response_model=list[TrackAll], tags=["Search"])
def search_tracks(*, db: Session = Depends(get_session), data: SearchTracks):
    tracks = db.exec(select(Track).filter(Track.trackURL.like("%"+data.term+"%"))).all()
    return tracks
