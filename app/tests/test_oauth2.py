from .. import oauth2
from fastapi import HTTPException

def test_create_access_token():
    data = {"user_id": "test_user_id", "privileged": False}
    token = oauth2.create_acces_token(data)
    assert token is not None

def test_verify_access_token_valid():
    data = {"user_id": "test_user_id", "privileged": False}
    token = oauth2.create_acces_token(data)
    token_data = oauth2.verify_access_token(token, None)
    assert token_data.id == "test_user_id"
    assert token_data.privileged == False

def test_verify_access_token_invalid():
    invalid_token = "invalid_token"
    credentials_exception = HTTPException(status_code=401, detail="Could not verify", headers={"WWW-Authenticate": "Bearer"})
    try:
        oauth2.verify_access_token(invalid_token, credentials_exception)
    except HTTPException as e:
        assert e.status_code == 401
        assert e.detail == "Could not verify"

def test_get_current_user_valid_token(client, test_user2):
    data = {"user_id": 1, "privileged": True}
    token = oauth2.create_acces_token(data)
    response = client.get("/users/myuser/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["privileged"] == False

def test_get_current_user_invalid_token(client):
    invalid_token = "invalid_token"
    response = client.get("/users/myuser/", headers={"Authorization": f"Bearer {invalid_token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not verify"
