from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import User, PlayHistory, Playlist, PlaylistTrack
from secure_api.schemas.schemas import DeleteUser, EditUser, UserWithPlaylistsPlayHistory, UserFull
from sqlmodel import Session, select

from fastapi_pagination.links import Page
from fastapi_pagination.ext.sqlmodel import paginate


users_router = APIRouter(dependencies=[Depends(get_currentUser)])


@users_router.get("/users", summary="Get array[] of all users",
                  response_model=Page[UserFull], tags=["User"])
def get_users(*, db: Session = Depends(get_session)):
    return paginate(db, select(User))


@users_router.get("/user/{userID}", summary="Get details of a single user",
                  response_model=UserWithPlaylistsPlayHistory, tags=["User"])
def get_user_userID(*, db: Session = Depends(get_session), userID: int):
    user = db.exec(select(User).where(User.userID == userID)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@users_router.patch("/user/{userID}", summary="Edit a user's username",
                    response_model=User, tags=["User"])
def edit_user_userID(*, userID: int, data: EditUser,
                     db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    db_user = db.get(User, userID)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if ((me.userID != userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can edit other users")

    me.username = data.username
    db.add(me)
    db.commit()
    db.refresh(me)
    return me


@users_router.delete("/user/{userID}", summary="Delete a user",
                     response_model=DeleteUser, tags=["User"])
def delete_user_userID(*, userID: int,
                       db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    user = db.get(User, userID)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if ((me.userID != userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can delete other users")

    playlists = db.exec(select(Playlist).where(Playlist.userID == user.userID)).all()
    for p in playlists:
        for p_track in db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == p.playlistID)).all():
            db.delete(p_track)
        for p_play in db.exec(select(PlayHistory).where(PlayHistory.userID == user.userID)).all():
            db.delete(p_play)
        db.delete(p)
    db.delete(user)
    db.commit()
    return user


