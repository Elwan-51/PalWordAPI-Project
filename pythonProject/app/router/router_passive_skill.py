from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.connexion import get_db
from app.database import PassiveSkillDB


class RouterPassiveSkill:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/v1/passive_skills",
            tags=["PassiveSkills"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route("", self.get_all_passive_skills_view, methods=["GET"], response_model=List[PassiveSkillDB.PassiveSkillView])
        self.router.add_api_route("/id/{passive_skill_id}", self.get_passive_skill_by_id_view, methods=["GET"], response_model=PassiveSkillDB.PassiveSkillView)
        self.router.add_api_route("/name/{name}", self.get_passive_skill_by_name_view, methods=["GET"], response_model=PassiveSkillDB.PassiveSkillView)
        self.router.add_api_route("", self.post_passive_skill_view, methods=["POST"], response_model=PassiveSkillDB.PassiveSkillView, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/id/{passive_skill_id}", self.delete_passive_skill_view, methods=["DELETE"], response_model=PassiveSkillDB.PassiveSkillView)
        self.router.add_api_route("", self.update_passive_skill_view, methods=["PUT"], response_model=PassiveSkillDB.PassiveSkillView)

    @staticmethod
    async def get_all_passive_skills_view(db=Depends(get_db)) -> List[PassiveSkillDB.PassiveSkillView]:
        return PassiveSkillDB.get_all_passive_skills(db)

    @staticmethod
    async def get_passive_skill_by_id_view(passive_skill_id: int, db=Depends(get_db)) -> PassiveSkillDB.PassiveSkillView:
        passive_skill = PassiveSkillDB.get_passive_skill_by_id(db, passive_skill_id)
        if passive_skill is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PassiveSkill not found")
        return passive_skill

    @staticmethod
    async def get_passive_skill_by_name_view(name: str, db=Depends(get_db)) -> PassiveSkillDB.PassiveSkillView:
        passive_skill = PassiveSkillDB.get_passive_skill_by_name(db, name)
        if passive_skill is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PassiveSkill not found")
        return passive_skill

    @staticmethod
    async def post_passive_skill_view(passive_skill: PassiveSkillDB.PassiveSkillCreate, db=Depends(get_db)) -> PassiveSkillDB.PassiveSkillView:
        if PassiveSkillDB.get_passive_skill_by_name(db, passive_skill.name) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PassiveSkill already exists")
        if PassiveSkillDB.get_passive_skill_by_id(db, passive_skill.id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PassiveSkill already exists")
        passive_skill_db = PassiveSkillDB.post_passive_skill(db, passive_skill)
        return passive_skill_db

    @staticmethod
    async def delete_passive_skill_view(passive_skill_id: int, db=Depends(get_db)) -> PassiveSkillDB.PassiveSkillView:
        passive_skill = PassiveSkillDB.get_passive_skill_by_id(db, passive_skill_id)
        if passive_skill is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PassiveSkill not found")
        passive_skill = PassiveSkillDB.delete_passive_skill(db, passive_skill_id)
        return passive_skill

    @staticmethod
    async def update_passive_skill_view(passive_skill: PassiveSkillDB.PassiveSkillUpdate, db=Depends(get_db)) -> PassiveSkillDB.PassiveSkillView:
        passive_skill_db = PassiveSkillDB.get_passive_skill_by_id(db, passive_skill.id)
        if passive_skill_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PassiveSkill not found")
        passive_skill_db = PassiveSkillDB.update_passive_skill(db, passive_skill.id, passive_skill)
        return passive_skill_db


def initialize(app):
    app.include_router(RouterPassiveSkill().router)