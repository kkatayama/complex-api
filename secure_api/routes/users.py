from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session
from secure_api.models.models import User
from secure_api.schemas.schemas import EditUser, ChangePass, UserWithPlaylists  # , UserUpdate
from secure_api.auth.auth_api import get_current_user, verify_password, get_hashed_password


users_router = APIRouter(dependencies=[Depends(get_current_user)])


@users_router.get("/users", summary="Get array[] of all users", response_model=List[User], tags=["User"])
def read_users(*, db: Session = Depends(get_session)):
    users = db.exec(select(User)).all()
    return users


@users_router.get("/users/{user_id}", summary="Get details of a user", response_model=UserWithPlaylists, tags=["User"])
def read_user(*, db: Session = Depends(get_session), user_id: int):
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@users_router.patch("/users/{user_id}", summary="Edit user details", tags=["User"])
def edit_user(*, user_id: int, user: EditUser, db: Session = Depends(get_session), me: User = Depends(get_current_user)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if (user_id != me.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your user")

    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_dta)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@users_router.patch("/change-password", summary="Change password", tags=["User"])
def change_password(*, user: ChangePass, db: Session = Depends(get_session), me: User = Depends(get_current_user)):
    if not verify_password(user.old_password, me.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    if (user_id != me.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only edit your user")

    hashed_password = get_hashed_password(user.new_password)
    me.password = hashed_password
    db.add(me)
    db.commit()
    db.refresh(me)
    return me


@users_router.delete("/users/{user_id}", summary="Delete user", tags=["User"])
def delete_user(*, user_id: int, db: Session = Depends(get_session), me: User = Depends(get_current_user)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if (user_id != me.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your user")

    db.delete(db_user)
    db.commit()
    return {"ok": True}
