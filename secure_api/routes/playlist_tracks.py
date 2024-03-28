from datetime import datetime

from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session, engine
from secure_api.models.models import User, Playlist, PlaylistTrack, Track, Album, Artist
from secure_api.schemas.schemas import AddPlaylistTrack, PlaylistTrackFull, CreatePlaylist, PlaylistWithUser
from secure_api.auth.auth_api import get_currentUser


playlist_tracks_router = APIRouter(dependencies=[Depends(get_currentUser)])


@playlist_tracks_router.post("/playlistTracks", summary="Add a Track to a Playlist", response_model=PlaylistTrack, tags=["PlaylistTrack"])
def add_playlist_track(*, data: AddPlaylistTrack, db: Session = Depends(get_session)):
    playlist = db.get(Playlist, data.playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    track = db.get(Track, data.trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    db_playlist_track = PlaylistTrack(playlistID=data.playlistID, trackID=data.trackID, trackName=track.trackName,
                                      trackNumber=track.trackNumber, trackURL=track.trackURL, recordedDate=track.recordedDate,
                                      duration=track.duration, albumID=track.albumID, artistID=track.artistID)

    db.add(db_playlist_track)
    db.commit()
    db.refresh(db_playlist_track)
    return db_playlist_track

@playlist_tracks_router.get("/playlistTracks", response_model=List[PlaylistTrackFull], tags=["PlaylistTrack"])
def read_playlist_tracks(*, db: Session = Depends(get_session)):
    playlist_tracks = db.exec(select(PlaylistTrack)).all()
    return playlist_tracks


@playlist_tracks_router.get("/playlistTrack/{playlistID}", response_model=List[PlaylistTrackFull], tags=["PlaylistTrack"])
def read_playlist_track(*, playlistID: int, db: Session = Depends(get_session)):
    playlist_track = db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == playlistID)).all()
    return playlist_track
