from dateutil.parser import parse
from datetime import date
from pydantic import EmailStr
from typing import List, Optional
from sqlmodel import SQLModel


class TokenSchema(SQLModel):
    access_token: str
    access_expires: int
    refresh_token: str
    refresh_expires: int
    userID: int
    username: str
    userRole: str
    loginStatus: bool

class TokenPayload(SQLModel):
    exp: int
    sub: int
    role: str
    logged_in: bool

class RenewToken(SQLModel):
    token: str

class CreateUser(SQLModel):
    username: str
    password1: str
    password2: str

class UserFull(SQLModel):
    userID: int
    userRole: str
    username: str
    password: str
    loginStatus: bool

class UserNoPassword(SQLModel):
    userID: int
    userRole: str
    username: str
    loginStatus: bool

class LoginUser(SQLModel):
    username: str
    password: str

class EditUser(SQLModel):
    username: str

class ChangePass(SQLModel):
    oldPassword: str
    newPassword: str

class DeleteUser(UserFull):
    DELETED: bool = True

class UserSignOut(SQLModel):
    userID: int
    userRole: str
    username: str
    password: str
    loginStatus: bool = False

class ArtistBase(SQLModel):
    artistName: str
    artistPhotoURL: str

class ArtistFull(SQLModel):
    artistID: int
    artistName: str
    artistPhotoURL: str

class AlbumBase(SQLModel):
    albumID: int
    albumName: str
    numSongs: int
    year: int
    albumCoverURL: str

class AlbumFull(AlbumBase):
    artistID: int

class TrackBase(SQLModel):
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    genre: str
    recordedDate: str
    duration: str

class TrackFull(TrackBase):
    albumID: int
    artistID: int

class TrackExtended(TrackBase):
    artist: ArtistFull | None = None
    album: AlbumFull | None = None

class AlbumAll(AlbumBase):
    artist: ArtistFull | None = None
    tracks: list[TrackBase] | None = None

class AlbumTracks(SQLModel):
    albumID: int
    albumName: str
    numSongs: int
    year: int
    albumCoverURL: str
    artistID: int
    tracks: list[TrackFull] | None = None

class PlaylistBase(SQLModel):
    playlistID: int
    playlistName: str
    playlistLength: int
    creationDate: str

class PlaylistFull(PlaylistBase):
    userID: int

class PlaylistAll(PlaylistBase):
    user: UserNoPassword | None = None

class DeletePlaylist(PlaylistBase):
    DELETED: bool = True

class PlaylistTrackBase(SQLModel):
    playlistTrackID: int
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    recordedDate: str
    duration: str

class PlaylistTrackFull(PlaylistTrackBase):
    artistID: int
    albumID: int

class PlaylistTrackAll(PlaylistTrackBase):
    artist: ArtistFull | None = None
    album: AlbumBase | None = None

class CreatePlaylist(SQLModel):
    playlistName: str

class CreateUserPlaylist(SQLModel):
    userID: int
    playlistName: str

class RenamePlaylist(SQLModel):
    playlistName: str

class AddPlaylistTrack(SQLModel):
    trackID: int

class AddUserPlaylistTrack(SQLModel):
    userID: int
    trackID: int

class DeletePlaylistTrack(SQLModel):
    playlistTrackID: int

class DeletePlaylistTrack(PlaylistTrackBase):
    DELETED: bool = True


class PlayHistoryBase(SQLModel):
    playhistoryID: int
    playDate: str
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    recordedDate: str
    duration: str

class PlayHistoryFull(PlayHistoryBase):
    userID: int
    artistID: int
    albumID: int

class PlayHistoryExtended(PlayHistoryBase):
    user: UserFull | None = None
    artist: ArtistFull | None = None
    album: AlbumFull | None = None

class PlayHistoryNoUser(PlayHistoryBase):
    artist: ArtistFull | None = None
    album: AlbumFull | None = None

class PlayHistoryAddMyTrack(SQLModel):
    trackID: int

class PlayHistoryAddUserTrack(SQLModel):
    userID: int
    trackID: int

class ArtistWithAlbums(ArtistFull):
    albums: list[AlbumBase] | None = None


class ArtistWithAlbumTracks(ArtistFull):
    album: AlbumTracks | None = None

class AlbumWithTracks(AlbumBase):
    artist: ArtistFull | None = None
    tracks: list[TrackFull] | None = None

class ArtistWithAlbumsTracks(ArtistFull):
    album: AlbumAll | None = None


class TrackWithArtistAlbum(TrackExtended):
    artist: ArtistFull | None = None
    album: AlbumFull | None = None

class UserWithPlaylists(UserFull):
    playlists: list[PlaylistFull] | None = None

class UserWithPlaylistsPlayHistory(UserFull):
    playlists: list[PlaylistFull] | None = None
    playhistory: list[PlayHistoryFull] | None = None


class PlaylistWithUserTracks(PlaylistBase):
    user: UserFull | None = None
    tracks: list[PlaylistTrackFull] | None = None

class PlaylistWithUserTracksAll(PlaylistBase):
    user: UserFull | None = None
    tracks: list[PlaylistTrackAll] | None = None


# class PlaylistsFull(PlaylistTestFull):
#     tracks: list[PlaylistTrackBase] | None = None

class PlaylistsWithMyTracks(PlaylistBase):
    artist: ArtistFull | None = None

class PlaylistWithPlaylistTracks(PlaylistAll):
    tracks: list[PlaylistTrackAll] | None = None

class UserWithPlaylistsPlayHistoryAll(UserFull):
    playlists: list[PlaylistWithPlaylistTracks] | None = None
    playhistory: list[PlayHistoryFull] | None = None
