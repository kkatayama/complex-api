from dateutil.parser import parse
from datetime import date
from pydantic import EmailStr
from sqlalchemy.sql.operators import isfalse
from typing import List, Optional
from sqlmodel import SQLModel, Field


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
    username: str = Field(min_length=1)
    password1: str = Field(min_length=1)
    password2: str = Field(min_length=1)

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
    username: str = Field(min_length=1)

class ChangePass(SQLModel):
    oldPassword: str = Field(min_length=1)
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

class ArtistAll(ArtistBase):
    artistID: int

class ArtistExtraFull(ArtistFull):
    artistExtraID: int
    artistID: int
    genre: str
    info: str


class AlbumBase(SQLModel):
    albumID: int
    albumName: str
    numSongs: int
    year: int
    albumCoverURL: str

class AlbumFull(AlbumBase):
    artistID: int

class AlbumAll(AlbumBase):
    artist: ArtistFull | None = None

class AlbumExtraFull(AlbumBase):
    albumExtraID: int
    albumID: int
    genre: str
    info: str
    color: str


class SuggestedAlbumBase(SQLModel):
    suggestedAlbumID: int
    albumID: int
    albumName: str
    numSongs: int
    year: int
    albumCoverURL: str

class SuggestedAlbumFull(SuggestedAlbumBase):
    userID: int
    albumID: int

class SuggestedAlbumAll(SuggestedAlbumBase):
    user: UserFull | None = None
    album: AlbumAll | None = None


class SuggestedAlbumMyAdd(SQLModel):
    albumID: int

class SuggestedAlbumUserAdd(SQLModel):
    userID: int
    albumID: int

class SuggestedAlbumDelete(SQLModel):
    userID: int

class SuggestedAlbumDeleted(SuggestedAlbumBase):
    DELETE: bool = True


class SuggestedArtistBase(SQLModel):
    suggestedArtistID: int
    artistID: int
    artistName: str
    artistPhotoURL: str

class SuggestedArtistFull(SuggestedArtistBase):
    userID: int
    artistID: int

class SuggestedArtistAll(SuggestedArtistBase):
    user: UserFull | None = None
    artist: ArtistFull | None = None

class SuggestedArtistMyAdd(SQLModel):
    artistID: int

class SuggestedArtistUserAdd(SQLModel):
    userID: int
    artistID: int

class SuggestedArtistDelete(SQLModel):
    userID: int

class SuggestedArtistDeleted(SuggestedArtistBase):
    DELETE: bool = True

class TrackBase(SQLModel):
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    genre: str
    recordedDate: str
    duration: str
    isFavorite: int

class TrackFull(TrackBase):
    albumID: int
    artistID: int

class TrackAll(TrackBase):
    artist: ArtistAll | None = None
    album: AlbumBase | None = None

class TrackExtended(TrackBase):
    artist: ArtistFull | None = None
    album: AlbumBase | None = None


class AlbumTracks(SQLModel):
    albumID: int
    albumName: str
    numSongs: int
    year: int
    albumCoverURL: str
    # artistID: int
    tracks: list[TrackBase] | None = None

class PlaylistBase(SQLModel):
    playlistID: int
    playlistName: str
    playlistLength: int
    creationDate: str

class PlaylistFull(PlaylistBase):
    userID: int

class PlaylistAll(PlaylistBase):
    user: UserNoPassword | None = None

class DeletePlaylist(SQLModel):
    userID: int

class DeletedPlaylist(PlaylistBase):
    DELETED: bool = True

class PlaylistTrackBase(SQLModel):
    playlistTrackID: int
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    genre: str
    recordedDate: str
    duration: str

class PlaylistTrackFull(PlaylistTrackBase):
    artistID: int
    albumID: int

class PlaylistTrackAll(PlaylistTrackBase):
    artist: ArtistFull | None = None
    album: AlbumBase | None = None

class CreatePlaylist(SQLModel):
    playlistName: str = Field(min_length=1)

class CreateUserPlaylist(SQLModel):
    userID: int
    playlistName: str = Field(min_length=1)

class RenamePlaylist(SQLModel):
    playlistName: str = Field(min_length=1)

class AddPlaylistTrack(SQLModel):
    trackID: int

class AddUserPlaylistTrack(SQLModel):
    userID: int
    trackID: int

class DeletePlaylistTrack(SQLModel):
    playlistTrackID: int

class DeletedPlaylistTrack(PlaylistTrackBase):
    DELETED: bool = True


class PlayHistoryBase(SQLModel):
    playhistoryID: int
    playDate: str
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    genre: str
    recordedDate: str
    duration: str

class PlayHistoryFull(PlayHistoryBase):
    userID: int
    artistID: int
    albumID: int

class PlayHistoryExtended(PlayHistoryBase):
    user: UserFull | None = None
    artist: ArtistFull | None = None
    album: AlbumBase | None = None

class PlayHistoryNoUser(PlayHistoryBase):
    artist: ArtistFull | None = None
    album: AlbumFull | None = None

class PlayHistoryAddMyTrack(SQLModel):
    trackID: int

class PlayHistoryAddUserTrack(SQLModel):
    userID: int
    trackID: int

class FavoriteBase(SQLModel):
    favoriteID: int
    addDate: str
    trackID: int
    trackName: str
    trackNumber: int
    trackURL: str
    genre: str
    recordedDate: str
    duration: str

class FavoriteFull(FavoriteBase):
    userID: int
    artistID: int
    albumID: int

class FavoriteExtended(FavoriteBase):
    user: UserFull | None = None
    artist: ArtistFull | None = None
    album: AlbumBase | None = None

class FavoriteAll(FavoriteBase):
    tracks: list[FavoriteExtended] | None = None

class FavoriteAddMyTrack(SQLModel):
    trackID: int

class FavoriteAddUserTrack(SQLModel):
    userID: int
    trackID: int

class FavoriteDeleteTrack(SQLModel):
    userID: int

class FavoriteDeletedTrack(FavoriteBase):
    DELETE: bool = True

class ImageBase(SQLModel):
    imageID: int
    resolution: str
    imageURL: str
    imageType: str

class ImageFull(ImageBase):
    artistID: int
    albumID: int

class ImageAll(ImageBase):
    artist: ArtistAll | None = None
    album: AlbumBase | None = None

class ImagesTable(SQLModel):
    status: int
    msg: str
    data: list[ImageFull] | None = None

class ArtistWithAlbums(ArtistFull):
    albums: list[AlbumBase] | None = None

class ArtistWithAlbumTracks(ArtistFull):
    album: AlbumTracks | None = None

class AlbumWithTracks(AlbumAll):
    # artist: ArtistFull | None = None
    tracks: list[TrackBase] | None = None

class AlbumWithTracksExpanded(AlbumAll):
    tracks: list[TrackAll] | None = None

class AlbumsWithTracks(AlbumBase):
    tracks: list[TrackBase] | None = None



class AlbumsExtraTracks(AlbumExtraFull):
    tracks: list[TrackBase] | None = None



class ArtistWithAlbumsTracks(ArtistFull):
    albums: list[AlbumsWithTracks] | None = None

class ArtistExtraAlbumsTracks(ArtistExtraFull):
    albums: list[AlbumsExtraTracks] | None = None



class TrackWithArtistAlbum(TrackExtended):
    artist: ArtistFull | None = None
    album: AlbumFull | None = None

class UserWithPlaylists(UserFull):
    playlists: list[PlaylistFull] | None = None

class UserWithPlaylistsPlayHistory(UserFull):
    playlists: list[PlaylistFull] | None = None
    playhistory: list[PlayHistoryFull] | None = None
    favorites: list[FavoriteFull] | None = None


class PlaylistWithUserTracks(PlaylistBase):
    user: UserNoPassword | None = None
    tracks: list[PlaylistTrackFull] | None = None

class PlaylistWithUserTracksAll(PlaylistBase):
    user: UserNoPassword | None = None
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
    favorites: list[FavoriteFull] | None = None


class SearchTracks(SQLModel):
    term: str
