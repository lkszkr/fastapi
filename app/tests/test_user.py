import pytest
from app import schemas

# GETTING MY USER
def test_auth_get_my_user(authorized_client, test_user):
    res = authorized_client.get("/users/myuser/")
    
    user_data = res.json()
    for data in list(user_data):
        assert user_data[data] == test_user[data]
    assert res.status_code == 200

def test_unauth_get_my_user(client, test_user):
    res = client.get("/users/myuser/")
    assert res.status_code == 401


# UPDATING MY USER
@pytest.mark.parametrize("name, surname, email, password, status_code", [
    ("NewName", "NewSurname", "newemail123@mail.com", "newPassword123", 200),   # Correct email
    ("NewName", "NewSurname", "email321@mail2.com", "newPassword123", 406),     # Incorrect email
    ("NewName", "NewSurname", "email321@mail.com", "newPassword123", 200)      # Same email
])
def test_auth_update_my_user(authorized_client, test_user, test_user2 , name, surname, email ,password, status_code):
    data = {
        "name": name,
        "surname": surname,
        "email": email,
        "password": password 
    }
    res = authorized_client.put("/users/myuser/", json=data)
    if(email != "email321@mail2.com"):
        new_user = schemas.UserOut(**res.json())
        assert new_user.email == email
        assert new_user.name == name
        assert new_user.id == test_user["id"]
    assert res.status_code == status_code

def test_unauth_update_my_user(client, test_user):
    data = {
        "name": "NewName",
        "surname": "NewSurname",
        "email": "newemail123@mail.com",
        "password": "newPassword123" 
    }
    res = client.put("/users/myuser/", json=data)
    assert res.status_code == 401

def test_auth_get_my_posts(authorized_client, test_user, test_posts):
    res = authorized_client.get("/users/myuser/myposts/")

    def validate(post):
        return schemas.Post(**post)
    post_map = map(validate, res.json())
    posts_list = list(post_map)
    for post in posts_list:
        assert post.owner_id == test_user["id"]
    assert res.status_code == 200

def test_unauth_get_my_posts(client, test_user, test_posts):
    res = client.get("/users/myuser/myposts/")
    assert res.status_code == 401

def test_auth_get_my_payments(authorized_client, test_user, test_posts):
    res = authorized_client.get("/users/myuser/mypayments/")

    def validate(payment):
        return schemas.Payment(**payment)
    payment_map = map(validate, res.json())
    payment_list = list(payment_map)
    for payment in payment_list:
        assert payment.user_id == test_user["id"]
    assert res.status_code == 200

def test_unauth_get_my_payments(client, test_user, test_posts):
    res = client.get("/users/myuser/mypayments/")
    assert res.status_code == 401

# GETTING ONE USER
def test_get_one_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}/")
    user_data = res.json()
    for data in list(user_data):
        assert user_data[data] == test_user[data]
    assert res.status_code == 200

def test_get_one_user_not_exist(client):
    res = client.get("/users/9999/")
    assert res.status_code == 404