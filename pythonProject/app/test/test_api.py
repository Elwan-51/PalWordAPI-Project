from fastapi.testclient import TestClient
from app.database.connexion import Base, get_db
from app.main import app
from app.internal.password import oauth2_scheme
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker


client = TestClient(app)
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=True,
    future=True)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_oauth2_scheme():
    return "Bearer 1234"


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[oauth2_scheme] = override_oauth2_scheme


def setup():
    Base.metadata.create_all(bind=engine)




def teardown():
    Base.metadata.drop_all(bind=engine)



