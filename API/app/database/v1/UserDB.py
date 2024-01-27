from pydantic import BaseModel
from typing import Optional
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey


class UserDb(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)


Base.metadata.create_all(bind=engine)


class UserView(BaseModel):
    id: int
    username: str


class UserCreate(BaseModel):
    id: Optional[int] = None
    username: str


class UserUpdate(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None


def get_all_users(db):
    return db.query(UserDb).all()


def get_user_by_id(db, user_id):
    return db.query(UserDb).filter(UserDb.id == user_id).first()

def get_user_by_username(db, username):
    return db.query(UserDb).filter(UserDb.username == username).first()


def post_user(db, user: UserCreate):
    db_user = UserDb(**user.model_dump(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db, user_id):
    user = db.query(UserDb).filter(UserDb.id == user_id).first()
    db.delete(user)
    db.commit()
    return user


def update_user(db, user_id, user: UserUpdate):
    db.query(UserDb).filter(UserDb.id == user_id).update(user.model_dump(exclude_unset=True))
    db.commit()
    return get_user_by_id(db, user_id)