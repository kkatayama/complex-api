from pydantic import EmailStr
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship, AutoString


class Artist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    image_path: str = Field(index=True)

    # albums: List["Album"] = Relationship(back_populates="album")
    #albums: List["Album"] = Relationship(back_populates="songs")


class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    image_path: str = Field(index=True)
    artist_name: str = Field(index=True)

    #artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")

    # songs: List["Track"] = Relationship(back_populates="albums")


class Playlist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None

    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="playlists")

    # tracks: List["Track"] = Relationship(back_populates="playlist")


class Track(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    mp3_path: str = Field(index=True)
    recorded_date: str = Field(index=True)
    album_name: str = Field(index=True)
    artist_name: str = Field(index=True)

    # artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")
    # # artist: Optional[Artist] = Relationship(back_populates="artist")

    # album_id: Optional[int] = Field(default=None, foreign_key="album.id")
    # album: Optional[Album] = Relationship(back_populates="songs")

    # playlist_id: Optional[int] = Field(default=None, foreign_key="playlist.id")
    # playlist: Optional[Playlist] = Relationship(back_populates="tracks")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password: str

    playlists: List[Playlist] = Relationship(back_populates="owner")
