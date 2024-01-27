from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, String
from typing import Optional
from pydantic import BaseModel


class ElementDB(Base):
    __tablename__ = "element"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    img_path = Column(String, nullable=True)





class ElementView(BaseModel):
    id: int
    name: str
    img_path: Optional[str] = None


class ElementCreate(BaseModel):
    id: Optional[int] = None
    name: str
    img_path: Optional[str] = None


class ElementUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    img_path: Optional[str] = None


def get_all_elements(db):
    return db.query(ElementDB).all()


def get_element_by_id(db, element_id):
    return db.query(ElementDB).filter(ElementDB.id == element_id).first()


def get_element_by_name(db, name):
    return db.query(ElementDB).filter(ElementDB.name == name).first()


def post_element(db, element: ElementCreate):
    db_element = ElementDB(**element.model_dump(exclude_unset=True))
    db.add(db_element)
    db.commit()
    db.refresh(db_element)
    return db_element


def delete_element(db, element_id):
    element = db.query(ElementDB).filter(ElementDB.id == element_id).first()
    db.delete(element)
    db.commit()
    return element


def update_element(db, element_id, element: ElementUpdate):
    db.query(ElementDB).filter(ElementDB.id == element_id).update(element.model_dump(exclude_unset=True))
    db.commit()
    return get_element_by_id(db, element_id)



