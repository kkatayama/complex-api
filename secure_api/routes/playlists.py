from datetime import datetime

from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session, engine
from secure_api.models.models import User, Playlist, PlaylistTrack, Track, Album, Artist
from secure_api.schemas.schemas import PlaylistFull, CreatePlaylist, PlaylistWithUserTracks
from secure_api.auth.auth_api import get_currentUser


playlists_router = APIRouter(dependencies=[Depends(get_currentUser)])


@playlists_router.post("/playlists",
                       summary="Create a playlist",
                       response_model=Playlist, tags=["Playlist"])
def create_playlist(*, db: Session = Depends(get_session), playlistName: str, me: User = Depends(get_currentUser)):
    statement = select(Playlist).where(Playlist.userID == me.id).where(Playlist.playlistName == playlistName)
    if db.exec(statement).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'You already have a Playlist titled: "{playlistName}"')

    date = str(datetime.now().date())
    db_playlist = Playlist(playlistName=playlistName, playlistLength=0, creationDate=date, userID=me.id)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@playlists_router.get("/playlists",
                      summary="Get array[] of all playlists",
                      response_model=List[PlaylistFull], tags=["Playlist"])
def get_playlists(*, db: Session = Depends(get_session)):
    playlists = db.exec(select(Playlist)).all()
    return playlists

@playlists_router.get("/playlist/{playlistID}",
                      summary="Get details of a single playlist (with tracks)",
                      response_model=PlaylistWithUserTracks, tags=["Playlist"])
def get_playlist_playlistID(*, db: Session = Depends(get_session), playlistID: int):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    user = db.get(User, playlist.userID)
    tracks = db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == playlistID)).all()

    db_playlist = PlaylistWithUserTracks(**playlist.dict())
    db_playlist.user = user
    db_playlist.tracks = tracks
    return db_playlist


@playlists_router.post("/playlist/{playlistID}/track/{trackID}",
                       summary="Add a single track to a playlist",
                       response_model=PlaylistTrack, tags=["Playlist"])
def add_playlist_playlistID_track_trackID(*, playlistID: int, trackID: int, db: Session = Depends(get_session)):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    track = db.get(Track, trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    db_playlist_track = PlaylistTrack(playlistID=playlistID, trackID=trackID, trackName=track.trackName,
                                      trackNumber=track.trackNumber, trackURL=track.trackURL, recordedDate=track.recordedDate,
                                      duration=track.duration, albumID=track.albumID, artistID=track.artistID)

    db.add(db_playlist_track)
    db.commit()
    db.refresh(db_playlist_track)
    return db_playlist_track
