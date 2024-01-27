from pydantic import BaseModel
from typing import Optional
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class PalElementDB(Base):
    __tablename__ = "pal_element"
    pal_id = Column(String, ForeignKey("pal.id"), primary_key=True)
    element_id = Column(Integer, ForeignKey("element.id"), primary_key=True)
    pal = relationship("PalDB", backref=backref("pal_element", cascade="all, delete"))
    element = relationship("ElementDB", backref=backref("pal_element", cascade="all, delete"))

class PalElementView(BaseModel):
    pal_id: str
    element_id: int


class PalElementCreate(BaseModel):
    pal_id: str
    element_id: int


def get_all_pal_elements(db):
    return db.query(PalElementDB).all()


def get_pal_element_by_id(db, pal_id, element_id):
    return db.query(PalElementDB).filter(PalElementDB.pal_id == pal_id, PalElementDB.element_id == element_id).first()


def get_pal_element_by_pal_id(db, pal_id):
    return db.query(PalElementDB).filter(PalElementDB.pal_id == pal_id).all()


def get_pal_element_by_element_id(db, element_id):
    return db.query(PalElementDB).filter(PalElementDB.element_id == element_id).all()


def post_pal_element(db, pal_element: PalElementCreate):
    db_pal_element = PalElementDB(**pal_element.model_dump(exclude_unset=True))
    db.add(db_pal_element)
    db.commit()
    db.refresh(db_pal_element)
    return db_pal_element


def delete_pal_element(db, pal_id, element_id):
    pal_element = db.query(PalElementDB).filter(PalElementDB.pal_id == pal_id, PalElementDB.element_id == element_id).first()
    db.delete(pal_element)
    db.commit()
    return pal_element


