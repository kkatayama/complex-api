from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Playlist, PlaylistTrack, Track, User
from secure_api.schemas.schemas import (AddUserPlaylistTrack, CreateUserPlaylist,
                                        DeletePlaylist, PlaylistFull,
                                        PlaylistWithUserTracks, RenamePlaylist)
from sqlmodel import Session, select

playlists_router = APIRouter(dependencies=[Depends(get_currentUser)])


@playlists_router.post("/playlist", summary="Create a playlist for a specified user",
                       response_model=Playlist, tags=["Playlist"])
def create_playlist(*, db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                    data: CreateUserPlaylist):
    statement = select(Playlist).where(Playlist.userID == data.userID).where(Playlist.playlistName == data.playlistName)
    if db.exec(statement).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User already has a Playlist titled: "{data.playlistName}"')
    if ((me.userID != data.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can create playlists for other users")

    date = str(datetime.now().date())
    db_playlist = Playlist(playlistName=data.playlistName, playlistLength=0, creationDate=date, userID=data.userID)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist

@playlists_router.get("/playlists", summary="Get array[] of all playlists for all users",
                      response_model=List[PlaylistFull], tags=["Playlist"])
def get_playlists(*, db: Session = Depends(get_session)):
    playlists = db.exec(select(Playlist)).all()
    return playlists


@playlists_router.post("/playlist/{playlistID}/tracks", summary="Add a single track to a user's playlist",
                       response_model=PlaylistTrack, tags=["Playlist"])
def addTrack_playlist_playlistID(*, db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                                 playlistID: int, data: AddUserPlaylistTrack):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    track = db.get(Track, data.trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Track not found (trackID={data.trackID})")
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can add tracks to another user's playlists")

    db_playlist_track = PlaylistTrack(playlistID=playlistID, trackID=data.trackID, trackName=track.trackName,
                                      trackNumber=track.trackNumber, trackURL=track.trackURL, recordedDate=track.recordedDate,
                                      duration=track.duration, albumID=track.albumID, artistID=track.artistID)

    playlist.playlistLength += 1
    db.add(playlist)
    db.add(db_playlist_track)
    db.commit()
    db.refresh(playlist)
    db.refresh(db_playlist_track)
    return db_playlist_track


@playlists_router.get("/playlist/{playlistID}", summary="Get details of a single playlist (with tracks)",
                      response_model=PlaylistWithUserTracks, tags=["Playlist"])
def get_playlist_playlistID(*, db: Session = Depends(get_session),
                            playlistID: int):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    user = db.get(User, playlist.userID)
    tracks = db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == playlistID)).all()

    db_playlist = PlaylistWithUserTracks(**playlist.dict())
    db_playlist.user = user
    db_playlist.tracks = tracks
    return db_playlist


@playlists_router.patch("/playlist/{playlistID}", summary="Rename a playlist",
                       response_model=Playlist, tags=["Playlist"])
def rename_playlist_playlistID(*, db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                               playlistID: int, data: RenamePlaylist):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    if db.exec(select(Playlist).where(Playlist.playlistName == data.playlistName)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User already has a Playlist titled: "{data.playlistName}"')
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can rename another user's playlists")

    playlist.playlistName = data.playlistName
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist



@playlists_router.delete("/playlist/{playlistID}", summary="Delete a single playlist",
                      response_model=DeletePlaylist, tags=["Playlist"])
def delete_playlist_playlistID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                               playlistID: int):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can delete another user's playlists")

    playlist = db.exec(select(Playlist).where(Playlist.userID == me.userID).where(Playlist.playlistID == playlistID)).first()
    if not playlist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged in user does not have access to this playlist")

    for track in db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == playlistID)).all():
        db.delete(track)
    db.delete(playlist)
    db.commit()
    return playlist
