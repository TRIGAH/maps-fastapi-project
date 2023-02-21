from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import engine,get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastapi_test'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)


TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)  

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()  

app.dependency_overrides[get_db] = override_get_db        

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get("message"))
    assert res.status_code == 200
    assert res.json().get("message") == "Welcome to My API"

def test_create_user():
    res = client.post("/users",json={"email":"test@gmail.com","password":"test123"})
    new_user = schemas.UserResponse(**res.json())  
    assert new_user.email == "test@gmail.com"  
    assert res.status_code == 201