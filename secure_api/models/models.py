from datetime import date
from pydantic import EmailStr
from typing import List, Optional, Annotated
from sqlmodel import Field, SQLModel, Relationship, AutoString


class Artist(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    artistName: str = Field(index=True)
    artistPhotoURL: str = Field(index=True)

    albums: list["Album"] = Relationship(back_populates="artist")
    # tracks: list["Track"] = Relationship(back_populates="artist")


class Album(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    albumName: str = Field(index=True)
    numSongs: int = Field(index=True)
    year: int = Field(index=True)
    albumCoverURL: str = Field(index=True)

    artistID: int | None = Field(default=None, foreign_key="artist.id")

    artist: Artist = Relationship(back_populates="albums")
    tracks: list["Track"] = Relationship(back_populates="album")


class Playlist(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    playlistName: str = Field(index=True)
    playlistLength: int
    creationDate: str = Field(index=True)

    userID: int | None = Field(default=None, foreign_key="user.id")
    # trackID: int | None = Field(default=None, foreign_key="track.id")

    user: "User" = Relationship(back_populates="playlists")
    # tracks: list["Track"] | None = Relationship(back_populates="playlists")


class PlaylistTrack(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    playlistID: int = Field(index=True)
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    recordedDate: str
    duration: str
    albumID: int
    artistID: int


class Track(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    trackName: str = Field(index=True)
    trackNumber: int
    trackURL: str = Field(index=True)
    recordedDate: str = Field(index=True)
    duration: str

    albumID: int | None = Field(default=None, foreign_key="album.id")
    artistID: int | None = Field(default=None, foreign_key="artist.id")

    album: Album | None = Relationship(back_populates="tracks")
    # artist: Artist | None  = Relationship(back_populates="tracks")
    # playlists: list[Playlist] | None = Relationship(back_populates="tracks")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    userRole: str
    username: str = Field(index=True)
    password: str
    loginStatus: bool

    playlists: list[Playlist] | None = Relationship(back_populates="user")
    playhistory: list["PlayHistory"] | None = Relationship(back_populates="user")

class Image(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    resolution: str
    imageURL: str = Field(index=True)
    imageType: str


class PlayHistory(SQLModel, table=True):
    entryID: int | None = Field(default=None, primary_key=True)
    userID: int | None = Field(default=None, foreign_key="user.id")
    playDate: str = Field(index=True)
    trackID: int | None = Field(default=None, foreign_key="track.id")
    trackName: str = Field(index=True)
    trackNumber: int
    trackURL: str = Field(index=True)
    recordedDate: str = Field(index=True)
    duration: str

    albumID: int | None = Field(default=None, foreign_key="album.id")
    artistID: int | None = Field(default=None, foreign_key="artist.id")

    user: User = Relationship(back_populates="playhistory")
