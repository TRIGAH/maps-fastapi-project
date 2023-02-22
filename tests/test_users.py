from app import schemas
from tests.database import client,session
import pytest

@pytest.fixture
def test_user(client):
    user_data = {"email":"maps@gmail.com","password":"maps"}
    res=client.post("/users/",json=user_data)
    assert res.status_code == 201
    print (res.json())
    new_user = res.json()
    new_user["password"]=user_data["password"]
    return new_user




def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.status_code == 200
    assert res.json().get("message") == "Welcome to My API"

def test_create_user(client):
    res = client.post("/users",json={"email":"test1@gmail.com","password":"test123"})
    new_user = schemas.UserResponse(**res.json())  
    assert new_user.email == "test1@gmail.com"  
    assert res.status_code == 201


def test_login_user(client,test_user):
    res = client.post("/login",data={"username":test_user["email"],"password":test_user["password"]})  
    assert res.status_code == 200  