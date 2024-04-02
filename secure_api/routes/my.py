from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from secure_api.auth.auth_api import (get_currentUser, get_hashed_password,
                                      verify_password)
from secure_api.database.database import get_session
from secure_api.models.models import (Album, Artist, PlayHistory, Playlist,
                                      PlaylistTrack, Track, User)
from secure_api.schemas.schemas import (AddMyPlaylistTrack, ChangePass,
                                        CreatePlaylist, DeleteMyPlaylistTrack,
                                        DeletePlaylist, DeletePlaylistTrack,
                                        DeleteUser, EditUser,
                                        PlayHistoryAddMyTrack,
                                        PlayHistoryExtended, PlayHistoryFull,
                                        PlaylistBase, PlaylistTrackAll,
                                        PlaylistTrackFull, PlaylistAll,
                                        PlaylistWithPlaylistTracks,
                                        PlaylistWithUserTracks,
                                        PlaylistWithUserTracksAll,
                                        RenamePlaylist, UserFull,
                                        UserWithPlaylistsPlayHistory,
                                        UserWithPlaylistsPlayHistoryAll)
from sqlmodel import Session, select

my_router = APIRouter(dependencies=[Depends(get_currentUser)])


@my_router.get("/my/user-info", summary="Get basic info of currently logged in user",
               response_model=UserFull, tags=["My-User"])
def get_my_user(*, me: User = Depends(get_currentUser)):
    return me


@my_router.get("/my/user-details", summary="Get detailed info of currently logged in user",
               response_model=UserWithPlaylistsPlayHistory, tags=["My-User"])
def get_my_userDetails(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    user = db.get(User, me.userID)
    return user


@my_router.get("/my/user-details-tracks", summary="Get detailed info of currently logged in user (with tracks expanded)",
               response_model=UserWithPlaylistsPlayHistoryAll, tags=["My-User"])
def get_my_userDetails_tracks(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    user = db.get(User, me.userID)
    return user


@my_router.patch("/my/username", summary="Modify username of currently logged in user",
                    response_model=User, tags=["My-User"])
def edit_my_username(*, data: EditUser, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    if db.exec(select(User).where(User.username == data.username)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exist")

    me.username = data.username
    db.add(me)
    db.commit()
    db.refresh(me)
    return me


@my_router.patch("/my/password", summary="Change a user's password",
                    response_model=User, tags=["My-User"])
def change_my_password(*, data: ChangePass, db: Session = Depends(get_session), me: User = Depends(get_currentUser)):
    if not verify_password(data.old_password, me.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    hashed_password = get_hashed_password(data.new_password)
    me.password = hashed_password
    db.add(me)
    db.commit()
    db.refresh(me)
    return me


@my_router.delete("/my/user", summary="Delete user account",
                  response_model=DeleteUser, tags=["My-User"])
def delete_my_user(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playlists = db.exec(select(Playlist).where(Playlist.userID == me.userID)).all()
    for p in playlists:
        for p_track in db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == p.playlistID)).all():
            db.delete(p_track)
        for p_play in db.exec(select(PlayHistory).where(PlayHistory.userID == me.userID)).all():
            db.delete(p_play)
    db.delete(me)
    db.commit()
    return me


@my_router.post("/my/playlist", summary="Create a playlist for the logged in user",
                       response_model=Playlist, tags=["My-Playlist"])
def create_my_playlist(*, db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                       data: CreatePlaylist):
    if db.exec(select(Playlist).where(Playlist.userID == me.userID).where(Playlist.playlistName == data.playlistName)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'You already have a Playlist titled: "{data.playlistName}"')

    date = str(datetime.now().date())
    db_playlist = Playlist(playlistName=data.playlistName, playlistLength=0, creationDate=date, userID=me.userID)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


@my_router.get("/my/playlists", summary="Get array[] of user's playlists",
               response_model=List[PlaylistAll], tags=["My-Playlist"])
def get_my_playlists(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playlists = db.exec(select(Playlist).where(Playlist.userID == me.userID)).all()
    return playlists


@my_router.get("/my/playlists/tracks", summary="Get array[] of user's playlists (with tracks expanded)",
               response_model=List[PlaylistWithPlaylistTracks], tags=["My-Playlist"])
def get_my_playlists_tracks(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playlists = db.exec(select(Playlist).where(Playlist.userID == me.userID)).all()
    return playlists

    # db_playlists = []
    # for playlist in playlists:
    #     tracks = db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == playlist.playlistID)).all()

    #     db_tracks = []
    #     for track in tracks:
    #         artist = db.get(Artist, track.artistID)
    #         album = db.get(Album, track.albumID)
    #         db_tracks.append(PlaylistTrackAll(**track.dict(), artist=artist, album=album))
    #     db_playlist = PlaylistWithPlaylistTracks(**playlist.dict(), user=me, tracks=db_tracks)
    #     db_playlists.append(db_playlist)
    # return db_playlists


@my_router.patch("/my/playlist/{playlistID}", summary="Rename a user's playlist",
                       response_model=Playlist, tags=["My-Playlist"])
def rename_my_playlist_playlistID(*, db: Session = Depends(get_session), me: User = Depends(get_currentUser),
                                  playlistID: int, data: RenamePlaylist):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    if db.exec(select(Playlist).where(Playlist.playlistName == data.playlistName)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'You already have a Playlist titled: "{data.playlistName}"')
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged in user does not have access to this playlist")

    playlist.playlistName = data.playlistName
    db.add(playlist)
    db.commit()
    db.refresh(playlist)
    return playlist


@my_router.get("/my/playlist/{playlistID}", summary="Get details of a single playlist (with tracks)",
               response_model=PlaylistWithUserTracks, tags=["My-Playlist"])
def get_my_playlist_playlistID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                               playlistID: int):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged in user does not have access to this playlist")
    return playlist

    # tracks = db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == playlistID)).all()
    # db_playlist = PlaylistWithUserTracks(**playlist.dict(), user=me, tracks=tracks)
    # return db_playlist


@my_router.delete("/my/playlist/{playlistID}", summary="Delete a user's playlist",
               response_model=DeletePlaylist, tags=["My-Playlist"])
def delete_my_playlist_playlistID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                                  playlistID: int):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged in user does not have access to this playlist")

    for track in db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == playlistID)).all():
        db.delete(track)
    db.delete(playlist)
    db.commit()
    return playlist


@my_router.post("/my/playlist/{playlistID}/tracks", summary="Add a single track to a playlist",
                       response_model=PlaylistTrackFull, tags=["My-Playlist"])
def addTrack_my_playlist_playlistID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                                    playlistID: int, data: AddMyPlaylistTrack):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    track = db.get(Track, data.trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Track not found (trackID={data.trackID})")
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged in user does not have access to this playlist")

    db_playlist_track = PlaylistTrack(playlistID=playlistID, **track.dict())

    playlist.playlistLength += 1
    db.add(playlist)
    db.add(db_playlist_track)
    db.commit()
    db.refresh(playlist)
    db.refresh(db_playlist_track)
    return db_playlist_track


@my_router.get("/my/playlist/{playlistID}/tracks", summary="Get details of a single playlist (with tracks expanded)",
               response_model=PlaylistWithUserTracksAll, tags=["My-Playlist"])
def get_my_playlist_playlistID_tracks(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                               playlistID: int):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged in user does not have access to this playlist")

    return playlist
    # tracks = db.exec(select(PlaylistTrack).where(PlaylistTrack.playlistID == playlistID)).all()

    # db_tracks = []
    # for track in tracks:
    #     artist = db.get(Artist, track.artistID)
    #     album = db.get(Album, track.albumID)
    #     db_tracks.append(PlaylistTrackAll(**track.dict(), artist=artist, album=album))
    # db_playlist = PlaylistWithUserTracksAll(**playlist.dict(), user=me, tracks=db_tracks)
    # return db_playlist


@my_router.delete("/my/playlist/{playlistID}/tracks", summary="Delete a single track from a playlist",
               response_model=DeletePlaylistTrack, tags=["My-Playlist"])
def delete_my_playlist_playlistID_tracks(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                                         playlistID: int, data: DeleteMyPlaylistTrack):
    playlist = db.get(Playlist, playlistID)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist not found (playlistID={playlistID})")
    if ((playlist.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Logged in user does not have access to this playlist")
    playlist_track = db.get(PlaylistTrack, data.playlistTrackID)
    if not playlist_track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Playlist track not found (playlistTrackID={data.playlistTrackID})")

    playlist.playlistLength -= 1
    db.add(playlist)
    db.delete(playlist_track)
    db.commit()
    db.refresh(playlist)
    return playlist_track


@my_router.post("/my/play-history", summary="Add a track to logged in user's play history",
                response_model=PlayHistory, tags=["My-PlayHistory"])
def addTrack_my_play_history(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                            data: PlayHistoryAddMyTrack):
    track = db.get(Track, data.trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Track not found (trackID={data.trackID})")

    date = str(datetime.now().date())
    db_playhistory_entry = PlayHistory(userID=me.userID, playDate=date, **track.dict())
    db.add(db_playhistory_entry)
    db.commit()
    db.refresh(db_playhistory_entry)
    return db_playhistory_entry


@my_router.get("/my/play-history", summary="Get array[] of playhistory for currently logged in user",
               response_model=List[PlayHistoryFull], tags=["My-PlayHistory"])
def get_my_play_history(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playhistory = db.exec(select(PlayHistory).where(PlayHistory.userID == me.userID)).all()
    return playhistory


@my_router.get("/my/play-history-tracks", summary="Get array[] of playhistory for currently logged in user (with tracks expanded)",
               response_model=List[PlayHistoryExtended], tags=["My-PlayHistory"])
def get_my_play_history_tracks(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    playhistory = db.exec(select(PlayHistory).where(PlayHistory.userID == me.userID)).all()
    return playhistory


@my_router.get("/my/play-history/{playhistoryID}", summary="Get details of a play history entry for currently logged in user",
               response_model=PlayHistoryExtended, tags=["My-PlayHistory"])
def get_my_playhistory_playhistoryID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                                     playhistoryID: int):
    playhistory = db.get(PlayHistory, playhistoryID)
    if not playhistory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PlayHistory not found (playhistoryID={playhistoryID})")
    if ((me.userID != playhistory.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can view another user's play history details")

    return playhistory
    # user = db.get(User, playhistory.userID)
    # artist = db.get(Artist, playhistory.artistID)
    # album = db.get(Album, playhistory.albumID)

    # db_playhistory = PlayHistoryExtended(**playhistory.dict(), user=user, artist=artist, album=album)
    # return db_playhistory
