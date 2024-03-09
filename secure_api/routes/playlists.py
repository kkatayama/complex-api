from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException

from secure_api.database.database import get_session
from secure_api.models import models


playlists_router = APIRouter()


@playlists_router.post("/playlists/", response_model=models.PlaylistRead)
def create_playlist(*, session: Session = Depends(get_session), playlist: models.PlaylistCreate):
    print(f'\nplaylist = {playlist}\n')
    db_playlist = models.Playlist.model_validate(playlist)
    session.add(db_playlist)
    session.commit()
    session.refresh(db_playlist)
    return db_playlist


@playlists_router.get("/playlists/", response_model=List[models.PlaylistRead])
def read_playlists(*, session: Session = Depends(get_session)):
    playlists = session.exec(select(models.Playlist)).all()
    print(f'\nplaylists = {playlists}\n')
    return playlists


@playlists_router.get("/playlists/{playlist_id}", response_model=models.PlaylistWithUser)
def read_playlist(*, session: Session = Depends(get_session), playlist_id: int):
    playlist = session.get(models.Playlist, playlist_id)
    print(f'\nplaylist = {playlist}\n')
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist
