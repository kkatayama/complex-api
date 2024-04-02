from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Album, Artist, PlayHistory, Track, User
from secure_api.schemas.schemas import (PlayHistoryAddUserTrack,
                                        PlayHistoryExtended, PlayHistoryFull)
from sqlmodel import Session, select

playhistory_router = APIRouter(dependencies=[Depends(get_currentUser)])


@playhistory_router.post("/play-history", summary="Add a track to a user's play history",
                response_model=PlayHistory, tags=["PlayHistory"])
def add_playhistory_trackID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                            data: PlayHistoryAddUserTrack):
    track = db.get(Track, data.trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Track not found (trackID={data.trackID})")
    user = db.get(User, data.userID)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found (userID={data.userID})")
    if ((me.userID != data.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can add tracks to another user's play history")

    date = str(datetime.now().date())
    db_playhistory_entry = PlayHistory(userID=data.userID, playDate=date, **track.dict())
    db.add(db_playhistory_entry)
    db.commit()
    db.refresh(db_playhistory_entry)
    return db_playhistory_entry


@playhistory_router.get("/play-history", summary="Get array[] of playhistory for all user's",
               response_model=list[PlayHistoryFull], tags=["PlayHistory"])
def get_playhistory(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playhistory = db.exec(select(PlayHistory)).all()
    return playhistory


@playhistory_router.get("/play-history/tracks", summary="Get array[] of playhistory for all user's (with tracks expanded)",
               response_model=list[PlayHistoryExtended], tags=["PlayHistory"])
def get_playhistory_tracks(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playhistory = db.exec(select(PlayHistory)).all()

    db_playhistory = []
    for play in playhistory:
        user = db.get(User, play.userID)
        artist = db.get(Artist, play.artistID)
        album = db.get(Album, play.albumID)
        db_playhistory.append(PlayHistoryExtended(**play.dict(), user=user, artist=artist, album=album))
    return db_playhistory


@playhistory_router.get("/play-history/{playhistoryID}", summary="Get details of a single play history entry",
               response_model=PlayHistoryExtended, tags=["PlayHistory"])
def get_playhistory_playhistoryID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                                  playhistoryID: int):
    playhistory = db.get(PlayHistory, playhistoryID)
    if not PlayHistory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PlayHistory not found (playhistoryID={playhistoryID})")
    user = db.get(User, playhistory.userID)
    artist = db.get(Artist, playhistory.artistID)
    album = db.get(Album, playhistory.albumID)

    db_playhistory = PlayHistoryExtended(**playhistory.dict(), user=user, artist=artist, album=album)
    return db_playhistory
