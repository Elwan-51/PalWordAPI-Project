from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.connexion import get_db
from app.database.v2 import UserDB


class RouterUser:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/v1/users",
            tags=["Users"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route("", self.get_all_users_view, methods=["GET"], response_model=List[UserDB.UserView])
        self.router.add_api_route("/id/{user_id}", self.get_user_by_id_view, methods=["GET"], response_model=UserDB.UserView)
        self.router.add_api_route("/username/{username}", self.get_user_by_username_view, methods=["GET"], response_model=UserDB.UserView)
        self.router.add_api_route("", self.post_user_view, methods=["POST"], response_model=UserDB.UserView, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/id/{user_id}", self.delete_user_view, methods=["DELETE"], response_model=UserDB.UserView)
        self.router.add_api_route("", self.update_user_view, methods=["PUT"], response_model=UserDB.UserView)

    @staticmethod
    async def get_all_users_view(db=Depends(get_db)) -> List[UserDB.UserView]:
        return UserDB.get_all_users(db)

    @staticmethod
    async def get_user_by_id_view(user_id: int, db=Depends(get_db)) -> UserDB.UserView:
        user = UserDB.get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def get_user_by_username_view(username: str, db=Depends(get_db)) -> UserDB.UserView:
        user = UserDB.get_user_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @staticmethod
    async def post_user_view(user: UserDB.UserCreate, db=Depends(get_db)) -> UserDB.UserView:
        if UserDB.get_user_by_username(db, user.username) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        if UserDB.get_user_by_id(db, user.id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        user_db = UserDB.post_user(db, user)
        return user_db

    @staticmethod
    async def delete_user_view(user_id: int, db=Depends(get_db)) -> UserDB.UserView:
        user = UserDB.get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user = UserDB.delete_user(db, user_id)
        return user

    @staticmethod
    async def update_user_view(user: UserDB.UserUpdate, db=Depends(get_db)) -> UserDB.UserView:
        user_db = UserDB.get_user_by_id(db, user.id)
        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        user_db = UserDB.update_user(db, user.id, user)
        return user_db


def initialize(app):
    app.include_router(RouterUser().router)

