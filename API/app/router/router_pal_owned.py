from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.connexion import get_db
from app.database.v2 import UserDB, PalDB, PalOwnedDB


class RouterPalOwned:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/v1/pal_owned",
            tags=["PalOwned"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route("/user_id/{user_id}", self.get_all_pal_owned_view, methods=["GET"], response_model=List[
            PalOwnedDB.PalOwnedView])
        self.router.add_api_route("/{pal_owned_id}", self.get_pal_owned_by_id_view, methods=["GET"], response_model=PalOwnedDB.PalOwnedView)
        self.router.add_api_route("/pal_id/{pal_id}/user_id/{user_id}", self.get_pal_owned_by_pal_id_view, methods=["GET"], response_model=List[
            PalOwnedDB.PalOwnedView])
        self.router.add_api_route("", self.post_pal_owned_view, methods=["POST"], response_model=PalOwnedDB.PalOwnedView, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/pal_id/{pal_id}/user_id/{user_id}", self.delete_pal_owned_view, methods=["DELETE"], response_model=PalOwnedDB.PalOwnedView)
        self.router.add_api_route("/user_id/{user_id}", self.update_pal_owned_view, methods=["PUT"], response_model=PalOwnedDB.PalOwnedView)

    @staticmethod
    async def get_all_pal_owned_view(user_id: int, db=Depends(get_db)) -> List[PalOwnedDB.PalOwnedView]:
        return PalOwnedDB.get_all_pal_owned(db, user_id)

    @staticmethod
    async def get_pal_owned_by_id_view(pal_owned_id: int, db=Depends(get_db)) -> PalOwnedDB.PalOwnedView:
        pal_owned = PalOwnedDB.get_pal_owned_by_id(db, pal_owned_id)
        if pal_owned is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalOwned not found")
        return pal_owned

    @staticmethod
    async def get_pal_owned_by_pal_id_view(pal_id: int, user_id: int, db=Depends(get_db)) -> List[
        PalOwnedDB.PalOwnedView]:
        pal_owned = PalOwnedDB.get_pal_owned_by_pal_id(db, pal_id, user_id)
        if pal_owned is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalOwned not found")
        return pal_owned

    @staticmethod
    async def post_pal_owned_view(pal_owned: PalOwnedDB.PalOwnedCreate, db=Depends(get_db)) -> PalOwnedDB.PalOwnedView:
        if PalOwnedDB.get_pal_owned_by_id(db, pal_owned.id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PalOwned already exists")
        if PalDB.get_pal_by_id(db, pal_owned.pal_id) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pal not found")
        if UserDB.get_user_by_id(db, pal_owned.user_id) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
        pal_owned_db = PalOwnedDB.post_pal_owned(db, pal_owned)
        return pal_owned_db

    @staticmethod
    async def delete_pal_owned_view(pal_owned_id: int, user_id: int, db=Depends(get_db)) -> PalOwnedDB.PalOwnedView:

        pal_owned = PalOwnedDB.get_pal_owned_by_id(db, pal_owned_id)
        if pal_owned is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalOwned not found")
        if pal_owned.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="PalOwned not owned by user")
        pal_owned = PalOwnedDB.delete_pal_owned(db, pal_owned_id)
        return pal_owned

    @staticmethod
    async def update_pal_owned_view(user_id: int, pal_owned: PalOwnedDB.PalOwnedUpdate, db=Depends(get_db)) -> PalOwnedDB.PalOwnedView:
        pal_owned = PalOwnedDB.get_pal_owned_by_id(db, pal_owned.id)
        if pal_owned is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalOwned not found")
        if pal_owned.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="PalOwned not owned by user")
        pal_owned_db = PalOwnedDB.update_pal_owned(db, pal_owned.id, pal_owned)
        return pal_owned_db


def initialize(app):
    app.include_router(RouterPalOwned().router)
