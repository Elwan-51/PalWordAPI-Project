from pydantic import BaseModel
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from typing import Optional
from app.database.v2 import PalDB, PalOwnedPassiveSkillDB, PassiveSkillDB


class PalOwnedDB(Base):
    __tablename__ = "pal_owned"
    id = Column(Integer, primary_key=True, unique=True)
    pal_id = Column(String, ForeignKey("pal.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    pal = relationship("PalDB", backref=backref("pal_owned", cascade="all, delete"))
    user = relationship("UserDb", backref=backref("pal_owned", cascade="all, delete"))
    name = Column(String, nullable=False, unique=False)
    level = Column(Integer, nullable=False, unique=False, default=1)
    attack = Column(Integer, nullable=False, unique=False)
    defense = Column(Integer, nullable=False, unique=False)
    work_speed = Column(Integer, nullable=False, unique=False)
    lucky = Column(Boolean, nullable=False, unique=False, default=False)
    boss = Column(Boolean, nullable=False, unique=False, default=False)


PalOwnedDB.passive_skills = relationship("PassiveSkillDB", secondary=PalOwnedPassiveSkillDB.PalOwnedPassiveSkillDB.__tablename__)

Base.metadata.create_all(bind=engine)


class PalOwnedView(BaseModel):
    id: int
    pal_id: str
    user_id: int
    name: str
    level: int
    attack: int
    defense: int
    work_speed: int
    lucky: bool
    boss: bool
    pal: PalDB.PalView
    passive_skills: list[PassiveSkillDB.PassiveSkillView]


class PalOwnedCreate(BaseModel):
    id: Optional[int] = None
    pal_id: str
    user_id: int
    name: str
    level: int
    attack: int
    defense: int
    work_speed: int
    lucky: Optional[bool] = False
    boss: Optional[bool] = False


class PalOwnedUpdate(BaseModel):
    id: Optional[int] = None
    pal_id: Optional[str] = None
    user_id: Optional[int] = None
    name: Optional[str] = None
    level: Optional[int] = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    work_speed: Optional[int] = None
    lucky: Optional[bool] = None
    boss: Optional[bool] = None



def get_all_pal_owned(db, user_id):
    return db.query(PalOwnedDB).filter(PalOwnedDB.user_id == user_id).all()


def get_pal_owned_by_id(db, pal_owned_id):
    return db.query(PalOwnedDB).filter(PalOwnedDB.id == pal_owned_id).first()


def get_pal_owned_by_pal_id(db, pal_id, user_id):
    return db.query(PalOwnedDB).filter(PalOwnedDB.pal_id == pal_id, PalOwnedDB.user_id == user_id).all()


def post_pal_owned(db, pal_owned: PalOwnedCreate):
    db_pal_owned = PalOwnedDB(**pal_owned.model_dump(exclude_unset=True))
    db.add(db_pal_owned)
    db.commit()
    db.refresh(db_pal_owned)
    return db_pal_owned


def delete_pal_owned(db, pal_owned_id):
    pal_owned = db.query(PalOwnedDB).filter(PalOwnedDB.id == pal_owned_id).first()
    db.delete(pal_owned)
    db.commit()
    return pal_owned


def update_pal_owned(db, pal_owned_id, pal_owned: PalOwnedUpdate):
    db.query(PalOwnedDB).filter(PalOwnedDB.id == pal_owned_id).update(pal_owned.model_dump(exclude_unset=True))
    db.commit()
    return get_pal_owned_by_id(db, pal_owned_id)




