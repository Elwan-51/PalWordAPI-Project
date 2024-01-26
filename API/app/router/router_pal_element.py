from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.connexion import get_db
from app.database import PalElementDB


class RouterPalElement:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/v1/pal_elements",
            tags=["PalElements"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route("", self.get_all_pal_elements_view, methods=["GET"], response_model=List[PalElementDB.PalElementView])
        self.router.add_api_route("/id/{pal_element_id}", self.get_pal_element_by_id_view, methods=["GET"], response_model=PalElementDB.PalElementView)
        self.router.add_api_route("/pal_id/{pal_id}", self.get_pal_element_by_pal_id_view, methods=["GET"], response_model=List[PalElementDB.PalElementView])
        self.router.add_api_route("/element_id/{element_id}", self.get_pal_element_by_element_id_view, methods=["GET"], response_model=List[PalElementDB.PalElementView])
        self.router.add_api_route("", self.post_pal_element_view, methods=["POST"], response_model=PalElementDB.PalElementView, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/element_id/{pal_element_id}", self.delete_pal_element_view, methods=["DELETE"], response_model=PalElementDB.PalElementView)

    @staticmethod
    async def get_all_pal_elements_view(db=Depends(get_db)) -> List[PalElementDB.PalElementView]:
        return PalElementDB.get_all_pal_elements(db)

    @staticmethod
    async def get_pal_element_by_id_view(pal_id: int, element_id: int, db=Depends(get_db)) -> PalElementDB.PalElementView:
        pal_element = PalElementDB.get_pal_element_by_id(db, pal_id, element_id)
        if pal_element is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalElement not found")
        return pal_element

    @staticmethod
    async def get_pal_element_by_pal_id_view(pal_id: int, db=Depends(get_db)) -> List[PalElementDB.PalElementView]:
        pal_element = PalElementDB.get_pal_element_by_pal_id(db, pal_id)
        if pal_element is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalElement not found")
        return pal_element

    @staticmethod
    async def get_pal_element_by_element_id_view(element_id: int, db=Depends(get_db)) -> List[PalElementDB.PalElementView]:
        pal_element = PalElementDB.get_pal_element_by_element_id(db, element_id)
        if pal_element is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalElement not found")
        return pal_element

    @staticmethod
    async def post_pal_element_view(pal_element: PalElementDB.PalElementCreate, db=Depends(get_db)) -> PalElementDB.PalElementView:
        if PalElementDB.get_pal_element_by_id(db, pal_element.pal_id, pal_element.element_id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PalElement already exists")
        pal_element_db = PalElementDB.post_pal_element(db, pal_element)
        return pal_element_db

    @staticmethod
    async def delete_pal_element_view(pal_id: int, element_id, db=Depends(get_db)) -> PalElementDB.PalElementView:
        pal_element = PalElementDB.get_pal_element_by_id(db, pal_id, element_id)
        if pal_element is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalElement not found")
        pal_element = PalElementDB.delete_pal_element(db, pal_id, element_id)
        return pal_element


def initialize(app):
    app.include_router(RouterPalElement().router)


