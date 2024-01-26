from pydantic import BaseModel
from typing import Optional
from app.database.connexion import Base, engine
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey


class PalDB(Base):
    __tablename__ = "pal"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String, nullable=False, unique=True)
    partner_skill = Column(String, nullable=True)
    kindling = Column(Integer, nullable=True)
    planting = Column(Integer, nullable=True)
    handwork = Column(Integer, nullable=True)
    lumbering = Column(Integer, nullable=True)
    medicine_production = Column(Integer, nullable=True)
    transporting = Column(Integer, nullable=True)
    watering = Column(Integer, nullable=True)
    generating_electricity = Column(Integer, nullable=True)
    gathering = Column(Integer, nullable=True)
    mining = Column(Integer, nullable=True)
    cooling = Column(Integer, nullable=True)
    farming = Column(Integer, nullable=True)
    farming_loot = Column(String, nullable=True)
    day_habitat_img = Column(String, nullable=True)
    night_habitat_img = Column(String, nullable=True)


Base.metadata.create_all(bind=engine)


class PalView(BaseModel):
    id: int
    name: str
    partner_skill: str
    kindling: int
    planting: int
    handwork: int
    lumbering: int
    medicine_production: int
    transporting: int
    watering: int
    generating_electricity: int
    gathering: int
    mining: int
    cooling: int
    farming: int
    farming_loot: str
    day_habitat_img: str
    night_habitat_img: str


class PalCreate(BaseModel):
    id: Optional[int] = None
    name: str
    partner_skill: Optional[str] = None
    kindling: Optional[int] = 0
    planting: Optional[int] = 0
    handwork: Optional[int] = 0
    lumbering: Optional[int] = 0
    medicine_production: Optional[int] = 0
    transporting: Optional[int] = 0
    watering: Optional[int] = 0
    generating_electricity: Optional[int] = 0
    gathering: Optional[int] = 0
    mining: Optional[int] = 0
    cooling: Optional[int] = 0
    farming: Optional[int] = 0
    farming_loot: Optional[str] = None
    day_habitat_img: Optional[str] = None
    night_habitat_img: Optional[str] = None


class PalUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    partner_skill: Optional[str] = None
    kindling: Optional[int] = None
    planting: Optional[int] = None
    handwork: Optional[int] = None
    lumbering: Optional[int] = None
    medicine_production: Optional[int] = None
    transporting: Optional[int] = None
    watering: Optional[int] = None
    generating_electricity: Optional[int] = None
    gathering: Optional[int] = None
    mining: Optional[int] = None
    cooling: Optional[int] = None
    farming: Optional[int] = None
    farming_loot: Optional[str] = None
    day_habitat_img: Optional[str] = None
    night_habitat_img: Optional[str] = None



def get_all_pals(db):
    return db.query(PalDB).all()


def get_pal_by_id(db, pal_id):
    return db.query(PalDB).filter(PalDB.id == pal_id).first()


def get_pal_by_name(db, name):
    return db.query(PalDB).filter(PalDB.name == name).first()


def get_pal_by_work_type(db, work_type):
    return db.query(PalDB).filter(getattr(PalDB, work_type) > 0).all()


def get_pal_by_work_type_and_level(db, work_type, level):
    return db.query(PalDB).filter(getattr(PalDB, work_type) == level).all()


def get_pal_by_work_type_and_level_range(db, work_type, level_min, level_max):
    return db.query(PalDB).filter(getattr(PalDB, work_type) >= level_min, getattr(PalDB, work_type) <= level_max).all()


def get_pal_by_work_type_and_level_min(db, work_type, level_min):
    return db.query(PalDB).filter(getattr(PalDB, work_type) >= level_min).all()


def post_pal(db, pal: PalCreate):
    db_pal = PalDB(**pal.model_dump(exclude_unset=True))
    db.add(db_pal)
    db.commit()
    db.refresh(db_pal)
    return db_pal


def delete_pal(db, pal_id):
    pal = db.query(PalDB).filter(PalDB.id == pal_id).first()
    db.delete(pal)
    db.commit()
    return pal


def update_pal(db, pal_id, pal: PalUpdate):
    db.query(PalDB).filter(PalDB.id == pal_id).update(pal.model_dump(exclude_unset=True))
    db.commit()
    return get_pal_by_id(db, pal_id)

