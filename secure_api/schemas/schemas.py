from dateutil.parser import parse
from datetime import date
from pydantic import EmailStr
from typing import List, Optional
from sqlmodel import SQLModel


class ArtistBase(SQLModel):
    artistName: str
    artistPhotoURL: str

class ArtistFull(ArtistBase):
    id: int

class CreateArtist(SQLModel):
    artistName: str
    artistPhotoURL: str


class AlbumBase(SQLModel):
    albumName: str
    numSongs: int
    year: int
    albumCoverURL: str
    artistID: int

class AlbumFull(AlbumBase):
    id: int

class CreateAlbum(SQLModel):
    albumName: str
    numSongs: int
    year: int
    albumCoverURL: str


class TrackBase(SQLModel):
    trackName: str
    trackNumber: int
    trackURL: str
    recordedDate: str
    duration: str
    albumID: int
    artistID: int

class TrackFull(TrackBase):
    id: int

class TrackExtended(SQLModel):
    trackName: str
    trackNumber: int
    trackURL: str
    recordedDate: str
    duration: str
    id: int

    albumID: int
    album: AlbumFull | None = None

    artistID: int
    artist: ArtistFull | None = None

class CreateTrack(SQLModel):
    trackName: str
    trackNumber: int
    trackURL: str
    recordedDate: str
    duration: str


class PlaylistBase(SQLModel):
    playlistName: str
    playlistLength: int
    creationDate: str
    userID: int

class PlaylistFull(PlaylistBase):
    id: int

class CreatePlaylist(SQLModel):
    playlistName: str

class EditPlaylist(SQLModel):
    playlistName: str


class PlaylistTrackBase(SQLModel):
    playlistID: int
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    recordedDate: str
    duration: str
    albumID: int
    artistID: int

class PlaylistTrackFull(PlaylistTrackBase):
    id: int

class AddPlaylistTrack(SQLModel):
    playlistID: int
    trackID: int

class UserBase(SQLModel):
    userRole: str
    username: str
    password: str
    loginStatus: bool

class UserFull(UserBase):
    id: int

class CreateUser(SQLModel):
    username: str
    password1: str
    password2: str

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


class AlbumTracks(SQLModel):
    albumName: str
    numSongs: int
    year: int
    albumCoverURL: str
    artistID: int
    id: int

    tracks: list[TrackFull] | None = None

class ArtistWithAlbums(ArtistFull):
    albums: list[AlbumFull] | None = None

class ArtistWithAlbumTracks(ArtistFull):
    album: AlbumTracks | None = None

class AlbumWithTracks(AlbumFull):
    tracks: list[TrackFull] | None = None

class TrackWithAlbumArtist(TrackFull):
    album: AlbumFull | None = None
    artist: ArtistFull | None = None


class UserWithPlaylists(UserFull):
    playlists: list[PlaylistFull] | None = None

class PlaylistWithUserTracks(PlaylistFull):
    user: UserFull | None = None
    tracks: list[PlaylistTrackFull] | None = None

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

"""
class Artist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    image_path: str = Field(index=True)

    # albums: List["Album"] = Relationship(back_populates="album")
    albums: List["Album"] = Relationship(back_populates="albums")


class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    release_date: str = Field(index=True)
    image_path: str = Field(index=True)

    artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")
    artist: Optional[Artist] = Relationship(back_populates="artist")

    tracks: List["Track"] = Relationship(back_populates="tracks")


class Track(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    release_date: str = Field(index=True)
    play_count: Optional[int] = Field(default=0)

    artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")
    artist: Optional[Artist] = Relationship(back_populates="artist")

    album_id: Optional[int] = Field(default=None, foreign_key="album.id")
    #album: Optional[Album] = Relationship(back_populates="album")
"""
