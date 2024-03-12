from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
#from secure_api.models.models import Playlist, User # , Artist, Album, Track


class PlaylistBase(SQLModel):
    title: str
    description: Optional[str] = None

    owner_id: Optional[int] = None

class PlaylistFull(PlaylistBase):
    id: int

# class Playlist(PlaylistBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)

#     owner: Optional["User"] = Relationship(back_populates="playlists")

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistRead(PlaylistBase):
    id: int

class PlaylistUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None


class UserBase(SQLModel):
    name: Optional[str]
    email: EmailStr
    password: str

class UserFull(UserBase):
    id: int

class CreateUser(SQLModel):
    name: Optional[str] = None
    email: EmailStr
    password1: str
    password2: str

class EditUser(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class ChangePass(SQLModel):
    old_password: str
    new_password: str


class UserWithPlaylists(UserFull):
    playlists: List[PlaylistFull] = []

class PlaylistWithUser(PlaylistFull):
    owner: Optional[UserFull] = None


class TokenSchema(SQLModel):
    access_token: str
    refresh_token: str

class TokenPayload(SQLModel):
    sub: int
    exp: int


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
