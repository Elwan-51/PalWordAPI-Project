from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.connexion import get_db
from app.database.v2 import PalDB


class RouterPal:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/v1/pals",
            tags=["Pals"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route("", self.get_all_pals_view, methods=["GET"], response_model=List[PalDB.PalView])
        self.router.add_api_route("/id/{pal_id}", self.get_pal_by_id_view, methods=["GET"], response_model=PalDB.PalView)
        self.router.add_api_route("/name/{name}", self.get_pal_by_name_view, methods=["GET"], response_model=PalDB.PalView)
        self.router.add_api_route("", self.post_pal_view, methods=["POST"], response_model=PalDB.PalView, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/id/{pal_id}", self.delete_pal_view, methods=["DELETE"], response_model=PalDB.PalView)
        self.router.add_api_route("", self.update_pal_view, methods=["PUT"], response_model=PalDB.PalView)
        self.router.add_api_route("/work_type/{work_type}", self.get_pal_by_work_type_view, methods=["GET"], response_model=List[PalDB.PalView])
        self.router.add_api_route("/work_type/{work_type}/min/{level}", self.get_pal_by_work_type_and_min_level_view, methods=["GET"], response_model=List[PalDB.PalView])
        self.router.add_api_route("/work_type/{work_type}/max/{level}", self.get_pal_by_work_type_and_max_level_view, methods=["GET"], response_model=List[PalDB.PalView])
        self.router.add_api_route("/work_type/{work_type}/min/{level_min}/max/{level_max}", self.get_pal_by_work_type_and_level_range_view, methods=["GET"], response_model=List[PalDB.PalView])

    @staticmethod
    async def get_all_pals_view(db=Depends(get_db)) -> List[PalDB.PalView]:
        return PalDB.get_all_pals(db)

    @staticmethod
    async def get_pal_by_id_view(pal_id: str, db=Depends(get_db)) -> PalDB.PalView:
        pal = PalDB.get_pal_by_id(db, pal_id)
        if pal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pal not found")
        return pal

    @staticmethod
    async def get_pal_by_name_view(name: str, db=Depends(get_db)) -> PalDB.PalView:
        pal = PalDB.get_pal_by_name(db, name)
        if pal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pal not found")
        return pal

    @staticmethod
    async def get_pal_by_work_type_view(work_type: str, db=Depends(get_db)) -> List[PalDB.PalView]:
        pal = PalDB.get_pal_by_work(db, work_type)
        if pal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pal not found")
        return pal

    @staticmethod
    async def get_pal_by_work_type_and_min_level_view(work_type: str, level: int, db=Depends(get_db)) -> List[PalDB.PalView]:
        pal = PalDB.get_pal_by_work_min(db, work_type, level)
        if pal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pal not found")
        return pal

    @staticmethod
    async def get_pal_by_work_type_and_max_level_view(work_type: str, level: int, db=Depends(get_db)) -> List[PalDB.PalView]:
        pal = PalDB.get_pal_by_work_max(db, work_type, level)
        if pal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pal not found")
        return pal

    @staticmethod
    async def get_pal_by_work_type_and_level_range_view(work_type: str, level_min: int, level_max: int, db=Depends(get_db)) -> List[PalDB.PalView]:
        pal = PalDB.get_pal_by_work_range(db, work_type, level_min, level_max)
        if pal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pal not found")
        return pal

    @staticmethod
    async def post_pal_view(pal: PalDB.PalCreate, db=Depends(get_db)) -> PalDB.PalView:
        if PalDB.get_pal_by_name(db, pal.name) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pal already exists")
        if PalDB.get_pal_by_id(db, pal.id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pal already exists")
        pal_db = PalDB.post_pal(db, pal)
        return pal_db

    @staticmethod
    async def delete_pal_view(pal_id: str, db=Depends(get_db)) -> PalDB.PalView:
        pal = PalDB.get_pal_by_id(db, pal_id)
        if pal is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pal not found")
        pal = PalDB.delete_pal(db, pal_id)
        return pal

    @staticmethod
    async def update_pal_view(pal: PalDB.PalUpdate, db=Depends(get_db)) -> PalDB.PalView:
        pal_db = PalDB.get_pal_by_id(db, pal.id)
        if pal_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pal not found")
        pal_db = PalDB.update_pal(db, pal.id, pal)
        return pal_db


def initialize(app):
    app.include_router(RouterPal().router)