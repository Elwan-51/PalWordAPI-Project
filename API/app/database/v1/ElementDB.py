from pydantic import BaseModel
from typing import Optional
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, String


class ElementDB(Base):
    __tablename__ = "element"
    id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String, nullable=False)
    img_path = Column(String, nullable=True)



Base.metadata.create_all(bind=engine)


class ElementView(BaseModel):
    id: int
    type_name: str
    img_path: Optional[str] = None


class ElementCreate(BaseModel):
    id: Optional[int] = None
    type_name: str
    img_path: Optional[str] = None


class ElementUpdate(BaseModel):
    id: Optional[int] = None
    type_name: Optional[str] = None
    img_path: Optional[str] = None


def get_all_elements(db):
    return db.query(ElementDB).all()


def get_element_by_id(db, element_id):
    return db.query(ElementDB).filter(ElementDB.id == element_id).first()


def get_element_by_type_name(db, type_name):
    return db.query(ElementDB).filter(ElementDB.type_name == type_name).first()


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




