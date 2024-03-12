from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, Playlist
from secure_api.schemas.schemas import PlaylistFull, CreatePlaylist, PlaylistWithUser
from secure_api.auth.auth_api import get_current_user


playlists_router = APIRouter(dependencies=[Depends(get_current_user)])


@playlists_router.post("/playlists", summary="Create a playlist", response_model=Playlist, tags=["Playlist"])
def create_playlist(*, db: Session = Depends(get_session), playlist: CreatePlaylist, me: User = Depends(get_current_user)):
    statement = select(Playlist).where(Playlist.owner_id == me.id).where(Playlist.title == playlist.title)
    if db.exec(statement).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'You already have a Playlist titled: "{playlist.title}"')

    db_playlist = Playlist.model_validate(playlist)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@playlists_router.get("/playlists/", response_model=List[PlaylistFull], tags=["Playlist"])
def read_playlists(*, db: Session = Depends(get_session)):
    playlists = db.exec(select(Playlist)).all()
    return playlists

@playlists_router.get("/playlists/{playlist_id}", response_model=PlaylistWithUser, tags=["Playlist"])
def read_playlist(*, db: Session = Depends(get_session), playlist_id: int):
    playlist = db.get(Playlist, playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    return playlist

@playlists_router.get("/playlists/{playlist_id}/tracks", response_model=PlaylistWithUser, tags=["Playlist"])
def read_playlist_tracks(*, db: Session = Depends(get_session), playlist_id: int):
    playlist = db.get(Playlist, playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    return playlist
