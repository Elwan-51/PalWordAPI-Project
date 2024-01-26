from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.connexion import get_db
from app.database import ElementDB


class RouterElement:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/v1/elements",
            tags=["Elements"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route("", self.get_all_elements_view, methods=["GET"], response_model=List[ElementDB.ElementView])
        self.router.add_api_route("/id/{element_id}", self.get_element_by_id_view, methods=["GET"], response_model=ElementDB.ElementView)
        self.router.add_api_route("/type/{type_name}", self.get_element_by_type_name_view, methods=["GET"], response_model=ElementDB.ElementView)
        self.router.add_api_route("", self.post_element_view, methods=["POST"], response_model=ElementDB.ElementView, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/id/{element_id}", self.delete_element_view, methods=["DELETE"], response_model=ElementDB.ElementView)
        self.router.add_api_route("", self.update_element_view, methods=["PUT"], response_model=ElementDB.ElementView)


    @staticmethod
    async def get_all_elements_view(db=Depends(get_db)) -> List[ElementDB.ElementView]:
        return ElementDB.get_all_elements(db)

    @staticmethod
    async def get_element_by_id_view(element_id: int, db=Depends(get_db)) -> ElementDB.ElementView:
        element = ElementDB.get_element_by_id(db, element_id)
        if element is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Element not found")
        return element

    @staticmethod
    async def get_element_by_type_name_view(type_name: str, db=Depends(get_db)) -> ElementDB.ElementView:
        element = ElementDB.get_element_by_type_name(db, type_name)
        if element is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Element not found")
        return element

    @staticmethod
    async def post_element_view(element: ElementDB.ElementCreate, db=Depends(get_db)) -> ElementDB.ElementView:
        if ElementDB.get_element_by_type_name(db, element.type_name) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Element already exists")
        if ElementDB.get_element_by_id(db, element.id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Element already exists")
        element_db = ElementDB.post_element(db, element)
        return element_db

    @staticmethod
    async def delete_element_view(element_id: int, db=Depends(get_db)) -> ElementDB.ElementView:
        element = ElementDB.get_element_by_id(db, element_id)
        if element is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Element not found")
        element = ElementDB.delete_element(db, element_id)
        return element

    @staticmethod
    async def update_element_view(element: ElementDB.ElementUpdate, db=Depends(get_db)) -> ElementDB.ElementView:
        element_db = ElementDB.get_element_by_id(db, element.id)
        if element_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Element not found")
        element_db = ElementDB.update_element(db, element.id, element)
        return element_db


def initialize(app):
    app.include_router(RouterElement().router)



