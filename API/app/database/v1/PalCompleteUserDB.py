from pydantic import BaseModel
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from typing import Optional


class PalCompleteUserDB(Base):
    __tablename__ = "pal_complete_user"
    pal_id = Column(Integer, ForeignKey("pal.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    pal = relationship("PalDB", backref=backref("pal_complete_user", cascade="all, delete"))
    user = relationship("UserDb", backref=backref("pal_complete_user", cascade="all, delete"))
    is_complete = Column(Boolean, nullable=False, default=False)


Base.metadata.create_all(bind=engine)


class PalCompleteUserView(BaseModel):
    pal_id: int
    user_id: int
    is_complete: bool


class PalCompleteUserCreate(BaseModel):
    pal_id: int
    user_id: int
    is_complete: Optional[bool] = False


class PalCompleteUserUpdate(BaseModel):
    pal_id: Optional[int] = None
    user_id: Optional[int] = None
    is_complete: Optional[bool] = None


def get_all_pal_complete_users(db):
    return db.query(PalCompleteUserDB).all()


def get_pal_complete_user_by_id(db, pal_id, user_id):
    return db.query(PalCompleteUserDB).filter(PalCompleteUserDB.pal_id == pal_id, PalCompleteUserDB.user_id == user_id).first()


def get_pal_complete_user_by_pal_id(db, pal_id):
    return db.query(PalCompleteUserDB).filter(PalCompleteUserDB.pal_id == pal_id).all()


def get_pal_complete_user_by_user_id(db, user_id):
    return db.query(PalCompleteUserDB).filter(PalCompleteUserDB.user_id == user_id).all()


def get_pal_complete_user_by_user_is_not_complete(db, user_id):
    return db.query(PalCompleteUserDB).filter(PalCompleteUserDB.user_id == user_id, PalCompleteUserDB.is_complete == False).all()


def post_pal_complete_user(db, pal_complete_user: PalCompleteUserCreate):
    db_pal_complete_user = PalCompleteUserDB(**pal_complete_user.model_dump(exclude_unset=True))
    db.add(db_pal_complete_user)
    db.commit()
    db.refresh(db_pal_complete_user)
    return db_pal_complete_user


def delete_pal_complete_user(db, pal_id, user_id):
    pal_complete_user = db.query(PalCompleteUserDB).filter(PalCompleteUserDB.pal_id == pal_id, PalCompleteUserDB.user_id == user_id).first()
    db.delete(pal_complete_user)
    db.commit()
    return pal_complete_user


def update_pal_complete_user(db, pal_id, user_id, pal_complete_user: PalCompleteUserUpdate):
    db.query(PalCompleteUserDB).filter(PalCompleteUserDB.pal_id == pal_id, PalCompleteUserDB.user_id == user_id).update(pal_complete_user.model_dump(exclude_unset=True))
    db.commit()
    return get_pal_complete_user_by_id(db, pal_id, user_id)

