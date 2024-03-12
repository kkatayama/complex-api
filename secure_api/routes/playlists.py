from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import Playlist
from secure_api.schemas.schemas import PlaylistRead, PlaylistCreate, PlaylistWithUser
from secure_api.auth.auth_api import get_current_user


playlists_router = APIRouter(dependencies=[Depends(get_current_user)])


@playlists_router.post("/playlists/", response_model=PlaylistRead, tags=["Playlist"])
def create_playlist(*, db: Session = Depends(get_session), playlist: PlaylistCreate):
    db_playlist = Playlist.model_validate(playlist)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


@playlists_router.get("/playlists/", response_model=List[PlaylistRead], tags=["Playlist"])
def read_playlists(*, db: Session = Depends(get_session)):
    playlists = db.exec(select(Playlist)).all()
    return playlists


@playlists_router.get("/playlists/{playlist_id}", response_model=PlaylistWithUser, tags=["Playlist"])
def read_playlist(*, db: Session = Depends(get_session), playlist_id: int):
    playlist = db.get(Playlist, playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    return playlist
