from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.connexion import get_db
from app.database.v2 import PalCompleteUserDB, UserDB, PalDB


class RouterPalCompleteUser:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/v1/pal_complete_users",
            tags=["PalCompleteUsers"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route("", self.get_all_pal_complete_users_view, methods=["GET"], response_model=List[
            PalCompleteUserDB.PalCompleteUserView])
        self.router.add_api_route("/pal_id/{pal_id}/user_id/{user_id}", self.get_pal_complete_user_by_id_view, methods=["GET"], response_model=PalCompleteUserDB.PalCompleteUserView)
        self.router.add_api_route("/pal_id/{pal_id}", self.get_pal_complete_user_by_pal_id_view, methods=["GET"], response_model=List[
            PalCompleteUserDB.PalCompleteUserView])
        self.router.add_api_route("/user_id/{user_id}", self.get_pal_complete_user_by_user_id_view, methods=["GET"], response_model=List[
            PalCompleteUserDB.PalCompleteUserView])
        self.router.add_api_route("/user_id/{user_id}/is_not_complete", self.get_pal_complete_user_by_user_is_not_complete_view, methods=["GET"], response_model=List[
            PalCompleteUserDB.PalCompleteUserView])
        self.router.add_api_route("", self.post_pal_complete_user_view, methods=["POST"], response_model=PalCompleteUserDB.PalCompleteUserCreate, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/pal_id/{pal_id}/user_id/{user_id}", self.delete_pal_complete_user_view, methods=["DELETE"], response_model=PalCompleteUserDB.PalCompleteUserView)
        self.router.add_api_route("", self.update_pal_complete_user_view, methods=["PUT"], response_model=PalCompleteUserDB.PalCompleteUserView)

    @staticmethod
    async def get_all_pal_complete_users_view(db=Depends(get_db)) -> List[PalCompleteUserDB.PalCompleteUserView]:
        return PalCompleteUserDB.get_all_pal_complete_users(db)

    @staticmethod
    async def get_pal_complete_user_by_id_view(pal_id: int, user_id: int, db=Depends(get_db)) -> PalCompleteUserDB.PalCompleteUserView:
        pal_complete_user = PalCompleteUserDB.get_pal_complete_user_by_id(db, pal_id, user_id)
        if pal_complete_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalCompleteUser not found")
        return pal_complete_user

    @staticmethod
    async def get_pal_complete_user_by_pal_id_view(pal_id: int, db=Depends(get_db)) -> List[
        PalCompleteUserDB.PalCompleteUserView]:
        pal_complete_user = PalCompleteUserDB.get_pal_complete_user_by_pal_id(db, pal_id)
        if pal_complete_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalCompleteUser not found")
        return pal_complete_user

    @staticmethod
    async def get_pal_complete_user_by_user_id_view(user_id: int, db=Depends(get_db)) -> List[
        PalCompleteUserDB.PalCompleteUserView]:
        pal_complete_user = PalCompleteUserDB.get_pal_complete_user_by_user_id(db, user_id)
        if pal_complete_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalCompleteUser not found")
        return pal_complete_user

    @staticmethod
    async def get_pal_complete_user_by_user_is_not_complete_view(user_id: int, db=Depends(get_db)) -> List[
        PalCompleteUserDB.PalCompleteUserView]:
        pal_complete_user = PalCompleteUserDB.get_pal_complete_user_by_user_is_not_complete(db, user_id)
        if pal_complete_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalCompleteUser not found")
        return pal_complete_user

    @staticmethod
    async def post_pal_complete_user_view(pal_complete_user: PalCompleteUserDB.PalCompleteUserCreate, db=Depends(get_db)) -> PalCompleteUserDB.PalCompleteUserView:
        if PalCompleteUserDB.get_pal_complete_user_by_id(db, pal_complete_user.pal_id, pal_complete_user.user_id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PalCompleteUser already exists")
        if PalDB.get_pal_by_id(db, pal_complete_user.pal_id) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pal not found")
        if UserDB.get_user_by_id(db, pal_complete_user.user_id) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

        pal_complete_user_db = PalCompleteUserDB.post_pal_complete_user(db, pal_complete_user)
        return pal_complete_user_db

    @staticmethod
    async def delete_pal_complete_user_view(pal_id: int, user_id, db=Depends(get_db)) -> PalCompleteUserDB.PalCompleteUserView:
        pal_complete_user = PalCompleteUserDB.get_pal_complete_user_by_id(db, pal_id, user_id)
        if pal_complete_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalCompleteUser not found")
        pal_complete_user = PalCompleteUserDB.delete_pal_complete_user(db, pal_id, user_id)
        return pal_complete_user

    @staticmethod
    async def update_pal_complete_user_view(pal_complete_user: PalCompleteUserDB.PalCompleteUserUpdate, db=Depends(get_db)) -> PalCompleteUserDB.PalCompleteUserView:
        pal_complete_user_db = PalCompleteUserDB.get_pal_complete_user_by_id(db, pal_complete_user.pal_id, pal_complete_user.user_id)
        if pal_complete_user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalCompleteUser not found")
        pal_complete_user_db = PalCompleteUserDB.update_pal_complete_user(db, pal_complete_user.pal_id, pal_complete_user.user_id, pal_complete_user)
        return pal_complete_user_db


def initialize(app):
    app.include_router(RouterPalCompleteUser().router)