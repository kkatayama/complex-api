from fastapi import APIRouter, Depends, HTTPException, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Album, Artist, PlayHistory, Track, User, Favorite, SuggestedAlbum, SuggestedArtist
from secure_api.schemas.schemas import (SuggestedAlbumFull, SuggestedAlbumAll, SuggestedArtistFull, SuggestedArtistAll,
                                        SuggestedAlbumUserAdd, SuggestedArtistUserAdd, SuggestedArtistDelete, SuggestedAlbumDelete,
                                        SuggestedArtistDeleted, SuggestedAlbumDeleted)
from sqlmodel import Session, select


suggested_router = APIRouter(dependencies=[Depends(get_currentUser)])


@suggested_router.post("/suggested-artist", summary="Add an Artist to SuggestedArtists on behalf of another user",
                       response_model=SuggestedArtist, tags=["Suggested-Artists"])
def add_suggested_artist(*, data: SuggestedArtistUserAdd, db: Session = Depends(get_session),
                         me: User = Depends(get_currentUser)):
    artist = db.get(Artist, data.artistID)
    if not artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Artist not found (artistID={data.artistID})")
    user = db.get(User, data.userID)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found (userID={data.userID})")
    if ((me.userID != data.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can add an Artist to another user's Suggested Artists")

    db_suggested_artist = SuggestedArtist(userID=data.userID, **artist.dict())
    db.add(db_suggested_artist)
    db.commit()
    db.refresh(db_suggested_artist)
    return db_suggested_artist


@suggested_router.get("/suggested-artists", summary="Get array[] of all Suggested Artists",
                      response_model=list[SuggestedArtistFull], tags=["Suggested-Artists"])
def get_suggested_artists(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    """
    Highly Recommended Artists from the Com-Plex Staff
    """
    suggested_artists = db.exec(select(SuggestedArtist)).all()
    return suggested_artists


@suggested_router.get("/suggested-artists-all", summary="Get array[] of all Suggested Artists (with user and artist expanded)",
                      response_model=list[SuggestedArtistAll], tags=["Suggested-Artists"])
def get_suggested_artists_all(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    """
    Highly Recommended Artists from the Com-Plex Staff
    """
    suggested_artists = db.exec(select(SuggestedArtist)).all()
    return suggested_artists


@suggested_router.get("/suggested-artists/{suggestedArtistID}", summary="Get details of a single Suggested Artist entry",
                      response_model=SuggestedArtistAll, tags=["Suggested-Artists"])
def get_suggested_artist(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                         suggestedArtistID: int):
    suggested_artist = db.get(SuggestedArtist, suggestedArtistID)
    if not suggested_artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Suggested Artist entry not found (suggestedArtistID={suggestedArtistID})")
    return suggested_artist


@suggested_router.delete("/suggested-artists/{suggestedArtistID}", summary="Delete a single artist from a user's Suggested Artists",
                      response_model=SuggestedArtistDeleted, tags=["Suggested-Artists"])
def delete_suggested_artist(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                         data: SuggestedArtistDelete, suggestedArtistID: int):
    suggested_artist = db.get(SuggestedArtist, suggestedArtistID)
    if not suggested_artist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Suggested Artist entry not found (suggestedArtistID={suggestedArtistID})")
    if ((me.userID != data.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can delete an Artist from another user's Suggested Artists")

    db.delete(suggested_artist)
    db.commit()
    return suggested_artist


@suggested_router.post("/suggested-album", summary="Add an Album to SuggestedAlbums on behalf of another user",
                       response_model=SuggestedAlbum, tags=["Suggested-Albums"])
def add_suggested_album(*, data: SuggestedAlbumUserAdd, db: Session = Depends(get_session),
                         me: User = Depends(get_currentUser)):
    album = db.get(Album, data.albumID)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Album not found (albumID={data.albumID})")
    user = db.get(User, data.userID)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found (userID={data.userID})")
    if ((me.userID != data.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can add an Album to another user's Suggested Albums")

    db_suggested_album = SuggestedAlbum(userID=data.userID, **album.dict())
    db.add(db_suggested_album)
    db.commit()
    db.refresh(db_suggested_album)
    return db_suggested_album


@suggested_router.get("/suggested-albums", summary="Get array[] of all Suggested Albums",
                      response_model=list[SuggestedAlbumFull], tags=["Suggested-Albums"])
def get_suggested_albums(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    """
    Highly Recommended Albums from the Com-Plex Staff
    """
    suggested_albums = db.exec(select(SuggestedAlbum)).all()
    return suggested_albums


@suggested_router.get("/suggested-albums-all", summary="Get array[] of all Suggested Albums (with user and album expanded)",
                      response_model=list[SuggestedAlbumAll], tags=["Suggested-Albums"])
def get_suggested_albums_all(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    """
    Highly Recommended Albums from the Com-Plex Staff
    """
    suggested_albums = db.exec(select(SuggestedAlbum)).all()
    return suggested_albums


@suggested_router.get("/suggested-albums/{suggestedAlbumID}", summary="Get details of a single Suggested Album entry",
                      response_model=SuggestedAlbumAll, tags=["Suggested-Albums"])
def get_suggested_album(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                         suggestedAlbumID: int):
    suggested_album = db.get(SuggestedAlbum, suggestedAlbumID)
    if not suggested_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Suggested Album entry not found (suggestedAlbumID={suggestedAlbumID})")
    return suggested_album


@suggested_router.delete("/suggested-albums/{suggestedAlbumID}", summary="Delete a single album from a user's Suggested Albums",
                      response_model=SuggestedAlbumDeleted, tags=["Suggested-Albums"])
def delete_suggested_album(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                         data: SuggestedAlbumDelete, suggestedAlbumID: int):
    suggested_album = db.get(SuggestedAlbum, suggestedAlbumID)
    if not suggested_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Suggested Album entry not found (suggestedAlbumID={suggestedAlbumID})")
    if ((me.userID != data.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can delete an Album from another user's Suggested Albums")

    db.delete(suggested_album)
    db.commit()
    return suggested_album
