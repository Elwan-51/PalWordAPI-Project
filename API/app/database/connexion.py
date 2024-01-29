import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session


SQLALCHEMY_DATABASE_URL = (f"postgresql+psycopg2://{os.environ.get('USER_DB', 'palworld_api')}:"
                           f"{os.environ.get('PASSWD_DB', '51Ez93oq41*!')}@"
                           f"{os.environ.get('SERVER_DB', '54.38.44.72')}:"
                           f"{os.environ.get('PORT_DB', '5432')}/"
                           f"{os.environ.get('NAME_DB', 'palworld')}")
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
