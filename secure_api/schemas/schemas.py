from pydantic import EmailStr
from typing import List, Optional
from sqlmodel import SQLModel


class CreateArtist(SQLModel):
    title: str
    image_path: str

class CreateAlbum(SQLModel):
    title: str
    image_path: str
    artist_name: str

class CreateTrack(SQLModel):
    title: str
    mp3_path: str
    recorded_date: str
    artist_name: str
    album_name: str


class PlaylistBase(SQLModel):
    title: str
    description: Optional[str] = None

    owner_id: Optional[int] = None

class PlaylistFull(PlaylistBase):
    id: int

class CreatePlaylist(SQLModel):
    title: str
    description: Optional[str] = None

class EditPlaylist(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None


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
    access_expires: int
    refresh_token: str
    refresh_expires: int
    user_id: int
    name: str
    email: EmailStr

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
