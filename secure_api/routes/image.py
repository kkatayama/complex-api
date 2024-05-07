from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from secure_api.auth.auth_api import get_currentUser
from secure_api.database.database import get_session
from secure_api.models.models import Album, Artist, Track, Image
from secure_api.schemas.schemas import ImageBase, ImageFull, ImageAll, ImagesTable
from sqlmodel import Session, select


images_router = APIRouter(dependencies=[Depends(get_currentUser)])


@images_router.get("/images", summary="Get array[] of all images", tags=["Image"],
                   response_model=List[ImageAll])
def get_images(*, db: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=8, le=1000)):
    images = db.exec(select(Image).offset(offset).limit(limit)).all()
    return images

@images_router.get("/images2", summary="Get array[] of all images", tags=["Image"],
                   response_model=ImagesTable)
def get_images2(*, db: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=8, le=1000)):
    images = db.exec(select(Image).offset(offset).limit(limit)).all()
    return {"status": 0, "msg": "", "data": images}


@images_router.get("/image/{imageID}", summary="Get details of a single image", tags=["Image"],
                   response_model=ImageAll, response_model_exclude_none=True)
def get_image_imageID(*, db: Session = Depends(get_session),
                      imageID: int):
    image = db.get(Image, imageID)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image
