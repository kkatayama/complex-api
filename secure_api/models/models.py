from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship


class PlaylistBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = None

    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Playlist(PlaylistBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    owner: Optional["User"] = Relationship(back_populates="playlists")

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistRead(PlaylistBase):
    id: int

class PlaylistUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    password: str
    play_count: Optional[int] = Field(default=0)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    playlists: List[Playlist] = Relationship(back_populates="owner")

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    play_count: Optional[int] = None


class UserWithPlaylists(UserRead):
    playlists: List[Playlist] = []

class PlaylistWithUser(PlaylistRead):
    owner: Optional[User] = None

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

    artist_id: Optional[int] = Field(default=None, foreign_key="artist.id")
    artist: Optional[Artist] = Relationship(back_populates="artist")

    album_id: Optional[int] = Field(default=None, foreign_key="album.id")
    #album: Optional[Album] = Relationship(back_populates="album")
"""
