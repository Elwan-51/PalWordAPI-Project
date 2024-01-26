from pydantic import BaseModel
from typing import Optional
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey


class PassiveSkillDB(Base):
    __tablename__ = "passive_skill"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    level = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)


class PassiveSkillView(BaseModel):
    id: int
    name: str
    description: str
    level: int


class PassiveSkillCreate(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    level: int


class PassiveSkillUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    level: Optional[int] = None


def get_all_passive_skills(db):
    return db.query(PassiveSkillDB).all()


def get_passive_skill_by_id(db, passive_skill_id):
    return db.query(PassiveSkillDB).filter(PassiveSkillDB.id == passive_skill_id).first()


def get_passive_skill_by_name(db, name):
    return db.query(PassiveSkillDB).filter(PassiveSkillDB.name == name).first()


def post_passive_skill(db, passive_skill: PassiveSkillCreate):
    db_passive_skill = PassiveSkillDB(**passive_skill.model_dump(exclude_unset=True))
    db.add(db_passive_skill)
    db.commit()
    db.refresh(db_passive_skill)
    return db_passive_skill


def delete_passive_skill(db, passive_skill_id):
    passive_skill = db.query(PassiveSkillDB).filter(PassiveSkillDB.id == passive_skill_id).first()
    db.delete(passive_skill)
    db.commit()
    return passive_skill


def update_passive_skill(db, passive_skill_id, passive_skill: PassiveSkillUpdate):
    db.query(PassiveSkillDB).filter(PassiveSkillDB.id == passive_skill_id).update(passive_skill.model_dump(exclude_unset=True))
    db.commit()
    return get_passive_skill_by_id(db, passive_skill_id)