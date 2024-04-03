from datetime import date
from pydantic import EmailStr
from typing import List, Optional, Annotated
from sqlmodel import Field, SQLModel, Relationship, AutoString


class Artist(SQLModel, table=True):
    artistID: int | None = Field(default=None, primary_key=True)
    artistName: str = Field(index=True)
    artistPhotoURL: str = Field(index=True)

    albums: list["Album"] = Relationship(back_populates="artist")

    song: "Track" = Relationship(back_populates="artist")
    ptrack: "PlaylistTrack" = Relationship(back_populates="artist")
    htrack: "PlayHistory" = Relationship(back_populates="artist")
    # tracks: list["Track"] = Relationship(back_populates="artist")


class Album(SQLModel, table=True):
    albumID: int | None = Field(default=None, primary_key=True)
    albumName: str = Field(index=True)
    numSongs: int = Field(index=True)
    year: int = Field(index=True)
    albumCoverURL: str = Field(index=True)

    artistID: int | None = Field(default=None, foreign_key="artist.artistID")

    artist: Artist = Relationship(back_populates="albums")
    tracks: list["Track"] = Relationship(back_populates="album")

    ptrack: "PlaylistTrack" = Relationship(back_populates="album")
    htrack: "PlayHistory" = Relationship(back_populates="album")


class Playlist(SQLModel, table=True):
    playlistID: int | None = Field(default=None, primary_key=True)
    playlistName: str = Field(index=True)
    playlistLength: int
    creationDate: str = Field(index=True)

    userID: int | None = Field(default=None, foreign_key="user.userID")

    user: "User" = Relationship(back_populates="playlists")
    tracks: list["PlaylistTrack"] = Relationship(back_populates="playlist")


class PlaylistTrack(SQLModel, table=True):
    playlistTrackID: int | None = Field(default=None, primary_key=True)
    playlistID: int | None = Field(index=True, foreign_key="playlist.playlistID")
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    recordedDate: str
    duration: str

    artistID: int | None = Field(default=None, foreign_key="artist.artistID")
    albumID: int | None = Field(default=None, foreign_key="album.albumID")

    playlist: Playlist | None = Relationship(back_populates="tracks")
    artist: Artist | None = Relationship(back_populates="ptrack")
    album: Album | None = Relationship(back_populates="ptrack")


class PlayHistory(SQLModel, table=True):
    playhistoryID: int | None = Field(default=None, primary_key=True)
    userID: int | None = Field(default=None, foreign_key="user.userID")
    playDate: str = Field(index=True)
    trackID: int | None = Field(default=None, foreign_key="track.trackID")
    trackName: str = Field(index=True)
    trackNumber: int
    trackURL: str = Field(index=True)
    recordedDate: str = Field(index=True)
    duration: str

    artistID: int | None = Field(default=None, foreign_key="artist.artistID")
    albumID: int | None = Field(default=None, foreign_key="album.albumID")

    user: "User" = Relationship(back_populates="playhistory")

    artist: Artist | None = Relationship(back_populates="htrack")
    album: Album | None = Relationship(back_populates="htrack")


class Track(SQLModel, table=True):
    trackID: int | None = Field(default=None, primary_key=True)
    trackName: str = Field(index=True)
    trackNumber: int
    trackURL: str = Field(index=True)
    genre: str
    recordedDate: str = Field(index=True)
    duration: str

    artistID: int | None = Field(default=None, foreign_key="artist.artistID")
    albumID: int | None = Field(default=None, foreign_key="album.albumID")

    album: Album | None = Relationship(back_populates="tracks")
    artist: Artist | None  = Relationship(back_populates="song")
    # playlists: list[Playlist] | None = Relationship(back_populates="tracks")


class User(SQLModel, table=True):
    userID: int | None = Field(default=None, primary_key=True)
    userRole: str
    username: str = Field(index=True)
    password: str
    loginStatus: bool

    playlists: list[Playlist] | None = Relationship(back_populates="user")
    playhistory: list[PlayHistory] | None = Relationship(back_populates="user")


class Image(SQLModel, table=True):
    imageID: int | None = Field(default=None, primary_key=True)
    resolution: str
    imageURL: str = Field(index=True)
    imageType: str

