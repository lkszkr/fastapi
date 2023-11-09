from app import schemas
from jose import jwt
from app.config import settings
import pytest

@pytest.mark.parametrize("name, surname, email, password, status_code", [
    ("Name", "Surname", "email123@mail.com", "Password123", 201),           # Correct email
    ("NewName", "NewSurname", "email321@mail.com", "newPassword123", 406)   # Incorrect email
])
def test_register(client, test_user, name, surname, email, password, status_code):
    res = client.post("/register", json={
        "name": name,
        "surname": surname,
        "email": email,
        "password": password 
        })
    if(email != "email321@mail.com"):
        new_user = schemas.UserOut(**res.json())
        assert new_user.email == email
    assert res.status_code == status_code

def test_login_user(client, test_user):
    res = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"] 
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key , algorithms=[settings.algorithm])
    id = payload.get("user_id")
    privileged = payload.get("privileged")
    assert id == test_user["id"]
    assert privileged == test_user["privileged"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("invalidemail@mail.com", "Password321", 403),      # Incorrect email
    ("email321@mail.com", "Invalid_password", 403),     # Incorrect password
    ("invalidemail@mail.com", "Invalid_password", 403), # Incorrect email
    (None, "Password321", 422),                         # No email
    ("email321@mail.com", None, 422)                    # No email

])
# test_user must be passed to create instace of a test user in the database
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password 
    })
    assert res.status_code == status_code