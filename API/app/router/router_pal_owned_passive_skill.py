from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database.connexion import get_db
from app.database.v2 import PassiveSkillDB, PalOwnedDB, PalOwnedPassiveSkillDB


class RouterPalOwnedPassiveSkill:
    def __init__(self):
        self.router = APIRouter(
            prefix="/api/v1/pal_owned_passive_skills",
            tags=["PalOwnedPassiveSkills"],
            responses={404: {"description": "Not found"}},
        )
        self.router.add_api_route("/pal_owned_id/{pal_owned_id}", self.get_all_pal_owned_passive_skills_by_pal_owned_id_view, methods=["GET"], response_model=List[
            PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView])
        self.router.add_api_route("/passive_skill_id/{passive_skill_id}", self.get_all_pal_owned_passive_skills_by_passive_skill_id_view, methods=["GET"], response_model=List[
            PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView])
        self.router.add_api_route("/pal_owned_id/{pal_owned_id}/passive_skill_id/{passive_skill_id}", self.get_pal_owned_passive_skill_by_id_view, methods=["GET"], response_model=PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView)
        self.router.add_api_route("", self.post_pal_owned_passive_skill_view, methods=["POST"], response_model=PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView, status_code=status.HTTP_201_CREATED)
        self.router.add_api_route("/pal_owned_id/{pal_owned_id}/passive_skill_id/{passive_skill_id}", self.delete_pal_owned_passive_skill_view, methods=["DELETE"], response_model=PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView)

    @staticmethod
    async def get_all_pal_owned_passive_skills_by_pal_owned_id_view(pal_owned_id: int, db=Depends(get_db)) -> List[
        PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView]:
        return PalOwnedPassiveSkillDB.get_all_pal_owned_passive_skills_by_pal_owned_id(db, pal_owned_id)

    @staticmethod
    async def get_all_pal_owned_passive_skills_by_passive_skill_id_view(passive_skill_id: int, db=Depends(get_db)) -> List[
        PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView]:
        return PalOwnedPassiveSkillDB.get_all_pal_owned_passive_skills_by_passive_skill_id(db, passive_skill_id)

    @staticmethod
    async def get_pal_owned_passive_skill_by_id_view(pal_owned_id: int, passive_skill_id: int, db=Depends(get_db)) -> PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView:
        pal_owned_passive_skill = PalOwnedPassiveSkillDB.get_pal_owned_passive_skill_by_id(db, pal_owned_id, passive_skill_id)
        if pal_owned_passive_skill is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalOwnedPassiveSkill not found")
        return pal_owned_passive_skill

    @staticmethod
    async def post_pal_owned_passive_skill_view(pal_owned_passive_skill: PalOwnedPassiveSkillDB.PalOwnedPassiveSkillCreate, db=Depends(get_db)) -> PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView:
        if PalOwnedPassiveSkillDB.get_pal_owned_passive_skill_by_id(db, pal_owned_passive_skill.pal_owned_id, pal_owned_passive_skill.passive_skill_id) is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PalOwnedPassiveSkill already exists")
        if PalOwnedDB.get_pal_owned_by_id(db, pal_owned_passive_skill.pal_owned_id) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PalOwned not found")
        if PassiveSkillDB.get_passive_skill_by_id(db, pal_owned_passive_skill.passive_skill_id) is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="PassiveSkill not found")
        pal_owned_passive_skill_db = PalOwnedPassiveSkillDB.post_pal_owned_passive_skill(db, pal_owned_passive_skill)
        return pal_owned_passive_skill_db

    @staticmethod
    async def delete_pal_owned_passive_skill_view(pal_owned_id: int, passive_skill_id: int, db=Depends(get_db)) -> PalOwnedPassiveSkillDB.PalOwnedPassiveSkillView:
        pal_owned_passive_skill = PalOwnedPassiveSkillDB.get_pal_owned_passive_skill_by_id(db, pal_owned_id, passive_skill_id)
        if pal_owned_passive_skill is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PalOwnedPassiveSkill not found")
        pal_owned_passive_skill = PalOwnedPassiveSkillDB.delete_pal_owned_passive_skill(db, pal_owned_id, passive_skill_id)
        return pal_owned_passive_skill


def initialize(app):
    app.include_router(RouterPalOwnedPassiveSkill().router)