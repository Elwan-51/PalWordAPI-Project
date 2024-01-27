from pydantic import BaseModel
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref


class PalOwnedPassiveSkillDB(Base):
    __tablename__ = "pal_owned_passive_skill"
    pal_owned_id = Column(Integer, ForeignKey("pal_owned.id"), primary_key=True)
    passive_skill_id = Column(Integer, ForeignKey("passive_skill.id"), primary_key=True)
    pal_owned = relationship("PalOwnedDB", backref=backref("pal_owned_passive_skill", cascade="all, delete"))
    passive_skill = relationship("PassiveSkillDB", backref=backref("pal_owned_passive_skill", cascade="all, delete"))


Base.metadata.create_all(bind=engine)


class PalOwnedPassiveSkillView(BaseModel):
    pal_owned_id: int
    passive_skill_id: int


class PalOwnedPassiveSkillCreate(BaseModel):
    pal_owned_id: int
    passive_skill_id: int


def get_all_pal_owned_passive_skills_by_pal_owned_id(db, pal_owned_id):
    return db.query(PalOwnedPassiveSkillDB).filter(PalOwnedPassiveSkillDB.pal_owned_id == pal_owned_id).all()


def get_all_pal_owned_passive_skills_by_passive_skill_id(db, passive_skill_id):
    return db.query(PalOwnedPassiveSkillDB).filter(PalOwnedPassiveSkillDB.passive_skill_id == passive_skill_id).all()


def get_pal_owned_passive_skill_by_id(db, pal_owned_id, passive_skill_id):
    return db.query(PalOwnedPassiveSkillDB).filter(PalOwnedPassiveSkillDB.pal_owned_id == pal_owned_id, PalOwnedPassiveSkillDB.passive_skill_id == passive_skill_id).first()


def post_pal_owned_passive_skill(db, pal_owned_passive_skill: PalOwnedPassiveSkillCreate):
    db_pal_owned_passive_skill = PalOwnedPassiveSkillDB(**pal_owned_passive_skill.model_dump(exclude_unset=True))
    db.add(db_pal_owned_passive_skill)
    db.commit()
    db.refresh(db_pal_owned_passive_skill)
    return db_pal_owned_passive_skill


def delete_pal_owned_passive_skill(db, pal_owned_id, passive_skill_id):
    pal_owned_passive_skill = db.query(PalOwnedPassiveSkillDB).filter(PalOwnedPassiveSkillDB.pal_owned_id == pal_owned_id, PalOwnedPassiveSkillDB.passive_skill_id == passive_skill_id).first()
    db.delete(pal_owned_passive_skill)
    db.commit()
    return pal_owned_passive_skill

