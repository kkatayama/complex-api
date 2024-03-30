from typing import List
from datetime import datetime, timedelta
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, Playlist, PlaylistTrack, Track, Album, Artist, PlayHistory
from secure_api.schemas.schemas import (
    CreateUser, LoginUser, EditUser, ChangePass, UserWithPlaylistsT, DeleteUser,
    PlaylistFull, PlaylistWithUserTracks, PlayHistoryFull, PlayHistoryExtended, PlayHistoryObj,
    TokenSchema, TokenPayload, RenewToken)
from secure_api.auth.auth_api import (
    get_currentUser, get_refreshUser, get_access_token, get_refresh_token, get_hashed_password,
    verify_password, create_access_token, create_refresh_token, reuseable_oauth)


my_router = APIRouter()


@my_router.get("/my/info",
               summary="Get basic info of currently logged in user",
               response_model=User, tags=["My"])
def get_my_info(*, me: User = Depends(get_currentUser)):
    return me


@my_router.get("/my/details",
               summary="Get detailed info of currently logged in user",
               response_model=UserWithPlaylistsT, tags=["My"])
def get_my_details(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    user = db.get(User, me.id)
    return user


@my_router.get("/my/playlists",
               summary="Get array[] of playlists for currently logged in user",
               response_model=List[PlaylistFull], tags=["My"])
def get_my_playlists(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playlists = db.exec(select(Playlist).where(Playlist.userID == me.id)).all()
    return playlists


@my_router.get("/my/play-history",
               summary="Get array[] of playhistory for currently logged in user",
               response_model=List[PlayHistoryObj], tags=["My"])
def get_my_playhistory(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playhistory = db.exec(select(PlayHistory).where(PlayHistory.userID == me.id)).all()
    return playhistory


@my_router.get("/my/play-history/{entryID}",
               summary="Get details of a play history entry for currently logged in user",
               response_model=PlayHistoryExtended, tags=["My"])
def get_my_playhistory_playhistoryID(*, entryID: int, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playhistory = db.get(PlayHistory, entryID)
    playhistory
    return playhistory


@my_router.post("/my/play-history/{trackID}",
                summary="Add a track to user's play history",
                response_model=PlayHistory, tags=["My"])
def add_my_playhistory_trackID(*, trackID: int, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    track = db.get(Track, trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    date = str(datetime.now().date())
    db_playhistory_entry = PlayHistory(userID=me.id, playDate=date, trackID=trackID, **track.dict())
    db.add(db_playhistory_entry)
    db.commit()
    db.refresh(db_playhistory_entry)
    return db_playhistory_entry


@my_router.patch("/my/change-username",
                    summary="Modify username of currently logged in user",
                    response_model=User, tags=["User"])
def edit_my_username(*, data: EditUser, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    me.username = data.username
    db.add(me)
    db.commit()
    db.refresh(me)
    return me


@my_router.patch("/my/change-password",
                    summary="Change a user's password",
                    response_model=User, tags=["My"])
def change_my_password(*, data: ChangePass, db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    if not verify_password(data.old_password, me.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    hashed_password = get_hashed_password(data.new_password)
    me.password = hashed_password
    db.add(me)
    db.commit()
    db.refresh(me)
    return me


