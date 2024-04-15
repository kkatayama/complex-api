from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Album, Artist, PlayHistory, Track, User, Favorite
from secure_api.schemas.schemas import (FavoriteAddUserTrack, FavoriteFull, FavoriteDeletedTrack,
                                        FavoriteExtended, FavoriteAll, FavoriteDeleteTrack)
from sqlmodel import Session, select

favorites_router = APIRouter(dependencies=[Depends(get_currentUser)])


@favorites_router.post("/favorites", summary="Add a track to a user's favorites list",
                response_model=Favorite, tags=["Favorite"])
def add_favorite(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                            data: FavoriteAddUserTrack):
    track = db.get(Track, data.trackID)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Track not found (trackID={data.trackID})")
    user = db.get(User, data.userID)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found (userID={data.userID})")
    if ((me.userID != data.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can add tracks to another user's play history")

    date = str(datetime.now().date())
    db_favorites_entry = Favorite(userID=data.userID, addDate=date, **track.dict())
    db.add(db_favorites_entry)
    db.commit()
    db.refresh(db_favorites_entry)
    return db_favorites_entry


@favorites_router.get("/favorites-all", summary="Get array[] of favorited tracks for all user's",
               response_model=list[FavoriteFull], tags=["Favorite"])
def get_favorites(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    favorites = db.exec(select(Favorite)).all()
    return favorites


@favorites_router.get("/favorites-tracks", summary="Get array[] of favorite tracks for all user's (with tracks expanded)",
               response_model=list[FavoriteExtended], tags=["Favorite"])
def get_favorites_tracks(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session)):
    favorites = db.exec(select(Favorite)).all()
    return favorites


@favorites_router.get("/favorites/{favoriteID}", summary="Get details of a single favorited entry",
               response_model=FavoriteExtended, tags=["Favorite"])
def get_favorite_favoriteID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                                  favoriteID: int):
    favorite = db.get(Favorite, favoriteID)
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Favorite entry not found (favoritesID={favoriteID})")
    return favorite


@favorites_router.delete("/favorites/{favoriteID}", summary="Delete a single track from a user's favorites",
                         response_model=FavoriteDeletedTrack, tags=["Favorite"])
def delete_favorite_favoriteID(*, me: User = Depends(get_currentUser), db: Session = Depends(get_session),
                                data: FavoriteDeleteTrack, favoriteID: int):
    favorite = db.get(Favorite, favoriteID)
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Favorite entry not found (favoritesID={favoriteID})")
    if ((data.userID != me.userID) and (me.userRole != "Administrator")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only an administrator can delete a track from another user's favorites")

    db.delete(favorite)
    db.commit()
    return favorite
