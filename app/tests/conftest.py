# Testing database setup
from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.main import app
from app.oauth2 import create_acces_token
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import settings
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # Before test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # Overriding database dependencies
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # After test

@pytest.fixture()
def test_user(client):
    user_data = {
        "name": "Name",
        "surname": "Surname",
        "email": "email321@mail.com",
        "password": "Password321" 
    }
    res = client.post("/register", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture()
def test_user2(client):
    user_data = {
        "name": "Name2",
        "surname": "Surname2",
        "email": "email321@mail2.com",
        "password": "Password321" 
    }
    res = client.post("/register", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

# Creating auth session for test_user
@pytest.fixture()
def token(test_user):
    return create_acces_token({
        "user_id": test_user["id"],
        "privileged": test_user["privileged"]
        })

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture()
def test_admin(client, session):
    user_data = {
        "name": "admin",
        "surname": "admin",
        "email": "admin@mail.com",
        "password": "Password321",
        "privileged": True
    }
    session.add(models.User(**user_data))
    session.commit()
    new_user = session.query(models.User).filter(models.User.privileged==True).first()
    return {"id": new_user.id, "privileged": new_user.privileged, "name": new_user.name, "email": new_user.email, "created_at": new_user.created_at}

@pytest.fixture()
def token_admin(test_admin):
    return create_acces_token({
        "user_id": test_admin["id"],
        "privileged": test_admin["privileged"]
        })

@pytest.fixture()
def authorized_admin(client, token_admin):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_admin}"
    }
    return client

@pytest.fixture()
def test_posts(test_user ,session, test_user2):
    posts_data = [
        {
            "title": "Test title",
            "content": "Test content",
            "goal": 100,
            "image": "encoodedString1",
            "owner_id": test_user["id"]
        },
        {
            "title": "Test title 2",
            "content": "Test content 2",
            "goal": 200,
            "image": "encoodedString3",
            "owner_id": test_user["id"]
        },
        {
            "title": "Test title 3",
            "content": "Test content 3",
            "goal": 300,
            "owner_id": test_user2["id"]
        },
    ]
    
    # Defining map for converting data into models.Post object that can be passed to session
    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    post = session.query(models.Post).all()
    return post

@pytest.fixture()
def test_payments(test_user, test_posts, session, test_user2):
    payments_data = [
        {
            "ammount": 10,
            "post_id": 1,
            "user_id": test_user["id"]
        },
        {
            "ammount": 20,
            "post_id": 1,
            "user_id": test_user["id"]
        },
        {
            "ammount": 30,
            "post_id": 2,
            "user_id": test_user2["id"]
        },
        {
            "ammount": 40,
            "post_id": 3,
            "user_id": test_user["id"]
        }
    ]
    
    # Defining map for converting data into models.Post object that can be passed to session
    def create_payment_model(payment):
        return models.Payments(**payment)
    payment_map = map(create_payment_model, payments_data)
    payments = list(payment_map)

    session.add_all(payments)
    session.commit()
    payment = session.query(models.Payments).all()
    return payment

