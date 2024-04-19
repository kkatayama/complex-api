from datetime import date
from pydantic import EmailStr
from typing import List, Optional, Annotated
from sqlmodel import Field, SQLModel, Relationship, TEXT, Column


class Artist(SQLModel, table=True):
    artistID: int | None = Field(default=None, primary_key=True)
    artistName: str = Field(index=True)
    artistPhotoURL: str = Field(index=True)

    albums: list["Album"] = Relationship(back_populates="artist")
    tracks: list["Track"] = Relationship(back_populates="artist")
    images: list["Image"] = Relationship(back_populates="artist")

    ptrack: "PlaylistTrack" = Relationship(back_populates="artist")
    htrack: "PlayHistory" = Relationship(back_populates="artist")
    ftrack: "Favorite" = Relationship(back_populates="artist")
    suggestedArtist: "SuggestedArtist" = Relationship(back_populates="artist")


class ArtistExtra(SQLModel, table=True):
    artistExtraID: int | None = Field(default=None, primary_key=True)
    artistID: int = Field(index=True)
    artistName: str = Field(index=True)
    artistPhotoURL: str = Field(index=True)
    genre: str
    info: str = Field(sa_column=Column(TEXT))

    albums: list["AlbumExtra"] = Relationship(back_populates="artist")
    tracks: list["TrackExtra"] = Relationship(back_populates="artist")


class Album(SQLModel, table=True):
    albumID: int | None = Field(default=None, primary_key=True)
    albumName: str = Field(index=True)
    numSongs: int = Field(index=True)
    year: int = Field(index=True)
    albumCoverURL: str = Field(index=True)

    artistID: int | None = Field(default=None, foreign_key="artist.artistID")

    artist: Artist = Relationship(back_populates="albums")
    tracks: list["Track"] = Relationship(back_populates="album")
    images: list["Image"] | None = Relationship(back_populates="album")

    ptrack: "PlaylistTrack" = Relationship(back_populates="album")
    htrack: "PlayHistory" = Relationship(back_populates="album")
    ftrack: "Favorite" = Relationship(back_populates="album")
    suggestedAlbum: "SuggestedAlbum" = Relationship(back_populates="album")


class AlbumExtra(SQLModel, table=True):
    albumExtraID: int | None = Field(default=None, primary_key=True)
    albumID: int | None = Field(index=True, nullable=False)
    albumName: str = Field(index=True)
    numSongs: int = Field(index=True)
    year: int = Field(index=True)
    albumCoverURL: str = Field(index=True)
    genre: str = Field(default=None)
    info: str = Field(sa_column=Column(TEXT))
    color: str = Field(default=None)

    artistExtraID: int | None = Field(default=None, foreign_key="artistextra.artistExtraID")

    artist: ArtistExtra = Relationship(back_populates="albums")
    tracks: list["TrackExtra"] = Relationship(back_populates="album")


class SuggestedArtist(SQLModel, table=True):
    suggestedArtistID: int | None = Field(default=None, primary_key=True)
    artistID: int | None = Field(default=None, foreign_key="artist.artistID")
    artistName: str = Field(index=True)
    artistPhotoURL: str = Field(index=True)
    userID: int | None = Field(default=None, foreign_key="user.userID")

    user: "User" = Relationship(back_populates="suggestedArtists")
    artist: Artist | None = Relationship(back_populates="suggestedArtist")


class SuggestedAlbum(SQLModel, table=True):
    suggestedAlbumID: int | None = Field(default=None, primary_key=True)
    albumID: int | None = Field(default=None, foreign_key="album.albumID")
    albumName: str = Field(index=True, nullable=False)
    numSongs: int
    year: int
    albumCoverURL: str = Field(index=True, nullable=False)
    userID: int | None = Field(default=None, foreign_key="user.userID")

    user: "User" = Relationship(back_populates="suggestedAlbums")
    album: Album | None = Relationship(back_populates="suggestedAlbum")


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
    genre: str
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
    genre: str
    recordedDate: str = Field(index=True)
    duration: str

    artistID: int | None = Field(default=None, foreign_key="artist.artistID")
    albumID: int | None = Field(default=None, foreign_key="album.albumID")

    user: "User" = Relationship(back_populates="playhistory")

    artist: Artist | None = Relationship(back_populates="htrack")
    album: Album | None = Relationship(back_populates="htrack")


class Favorite(SQLModel, table=True):
    favoriteID: int | None = Field(default=None, primary_key=True)
    userID: int | None = Field(default=None, foreign_key="user.userID")
    addDate: str = Field(index=True)
    trackID: int | None = Field(default=None, foreign_key="track.trackID")
    trackName: str = Field(index=True)
    trackNumber: int
    trackURL: str = Field(index=True)
    genre: str
    recordedDate: str = Field(index=True)
    duration: str

    artistID: int | None = Field(default=None, foreign_key="artist.artistID")
    albumID: int | None = Field(default=None, foreign_key="album.albumID")

    user: "User" = Relationship(back_populates="favorites")

    artist: Artist | None = Relationship(back_populates="ftrack")
    album: Album | None = Relationship(back_populates="ftrack")



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

    artist: Artist | None = Relationship(back_populates="tracks")
    album: Album | None = Relationship(back_populates="tracks")


class TrackExtra(SQLModel, table=True):
    trackExtraID: int | None = Field(default=None, primary_key=True)
    trackID: int = Field(index=True)
    trackName: str = Field(index=True)
    trackNumber: int
    trackURL: str = Field(index=True)
    genre: str
    recordedDate: str = Field(index=True)
    duration: str
    info: str = Field(sa_column=Column(TEXT))
    color: str = Field(default=None)

    artistExtraID: int | None = Field(default=None, foreign_key="artistextra.artistExtraID")
    albumExtraID: int | None = Field(default=None, foreign_key="albumextra.albumExtraID")

    artist: ArtistExtra | None = Relationship(back_populates="tracks")
    album: AlbumExtra | None = Relationship(back_populates="tracks")


class User(SQLModel, table=True):
    userID: int | None = Field(default=None, primary_key=True)
    userRole: str = Field(default="Customer")
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    loginStatus: bool = False

    playlists: list[Playlist] | None = Relationship(back_populates="user")
    playhistory: list[PlayHistory] | None = Relationship(back_populates="user")
    favorites: list[Favorite] | None = Relationship(back_populates="user")
    suggestedAlbums: list[SuggestedAlbum] | None = Relationship(back_populates="user")
    suggestedArtists: list[SuggestedArtist] | None = Relationship(back_populates="user")


class Image(SQLModel, table=True):
    imageID: int | None = Field(default=None, primary_key=True)
    resolution: str
    imageURL: str = Field(index=True)
    imageType: str

    artistID: int | None = Field(default=None, foreign_key="artist.artistID")
    albumID: int | None = Field(default=None, foreign_key="album.albumID")

    artist: Artist | None = Relationship(back_populates="images")
    album: Album | None = Relationship(back_populates="images")
