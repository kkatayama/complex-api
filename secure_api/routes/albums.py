from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User, Album, Artist, Track
from secure_api.schemas.schemas import AlbumFull, AlbumWithTracks
from secure_api.auth.auth_api import get_currentUser


albums_router = APIRouter(dependencies=[Depends(get_currentUser)])


@albums_router.get("/albums",
                   summary="Get array[] of all albums",
                   response_model=List[AlbumFull], tags=["Album"])
def get_albums(*, db: Session = Depends(get_session)):
    albums = db.exec(select(Album)).all()
    return albums

@albums_router.get("/album/{albumID}",
                   summary="Get details of a single album",
                   response_model=AlbumWithTracks, tags=["Album"])
def get_album_albumID(*, db: Session = Depends(get_session), albumID: int):
    album = db.get(Album, albumID)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album not found")
    return album

