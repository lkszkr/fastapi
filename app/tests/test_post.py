import pytest
from app import schemas

# GETTING POSTS
def test_auth_get_all_posts(authorized_client, test_posts, test_payments, test_user):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.Post(**post)
    post_map = map(validate, res.json())
    posts_list = list(post_map)

    # Fetching posts
    # Iterate through posts and test_posts
    for post, test_post in zip(posts_list, test_posts):
        for attr in ['id', 'title', 'content', 'goal', 'image', 'created_at']:
            assert getattr(post, attr) == getattr(test_post, attr)

    # Fetching payments
    # Iterate through posts and their payments to compare with test payments
    for post, test_post in zip(posts_list, test_posts):
        for payment in post.payments:
            # Next function is finding the first id in test_paymnet with matching id of paymnet.id
            test_payment = next((tp for tp in test_payments if tp.id == payment.id), None)
            if test_payment is not None:
                for attr in ['id', 'ammount', 'status', 'user_id', 'post_id']:
                    assert getattr(payment, attr) == getattr(test_payment, attr)
                    
    # Fetching user
    for attr in ['id', 'name', 'email', 'created_at', 'privileged']:
        if attr == 'created_at':
            # Date needs to be formated from datetime.datetime to str
            date = posts_list[0].owner.created_at
            formatted_date = date.strftime('%Y-%m-%dT%H:%M:%S.%f')
            assert formatted_date == test_user[attr]
        else:
            assert getattr(posts_list[0].owner, attr) == test_user[attr]

    # Lenght and status code
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauth_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_auth_get_one_posts(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = res.json()
    for attr in ['title', 'content', 'goal', 'image', 'id', 'created_at', 'owner_id']:
        if attr == 'created_at':
            date = test_posts[0].created_at
            formatted_date = date.strftime('%Y-%m-%dT%H:%M:%S.%f')
            assert post['created_at'] == formatted_date
        else:
            assert post[attr] == getattr(test_posts[0], attr)

    assert res.status_code == 200

def test_unauth_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    post = res.json()
    for attr in ['title', 'content', 'goal', 'image', 'id', 'created_at', 'owner_id']:
        if attr == 'created_at':
            date = test_posts[0].created_at
            formatted_date = date.strftime('%Y-%m-%dT%H:%M:%S.%f')
            assert post['created_at'] == formatted_date
        else:
            assert post[attr] == getattr(test_posts[0], attr)
    
    assert res.status_code == 200

def test_auth_get_one_posts_not_exist(authorized_client):
    res = authorized_client.get("/posts/99999")
    assert res.status_code == 404

def test_unauth_get_one_posts_not_exist(client):
    res = client.get("/posts/99999")
    assert res.status_code == 404

# CREATING POSTS
@pytest.mark.parametrize("title, content, goal, image",[
    ("New title", "New content", 99, "NewEncodedString"),
    ("New title2", "New content2", 999, None)
])
def test_auth_create_post(authorized_client, test_user, title, content, goal, image):
    res = authorized_client.post("/posts/", json={
        "title": title,
        "content": content,
        "goal": goal,
        "image": image
    })
    created_post = schemas.Post(**res.json())
    for attr, json_data in zip(['title', 'content', 'goal', 'image'], [title, content, goal, image]):    
        assert getattr(created_post, attr) == json_data
    if image is None:
        assert created_post.image == None
    assert created_post.owner_id == test_user["id"]
    assert created_post.payments == []
    assert res.status_code == 201

def test_unauth_create_post(client):
    res = client.post("/posts/", json={
        "title": "title",
        "content": "content",
        "goal": 0,
        "image": "image"
    })
    details = res.json()
    assert details["detail"] == "Not authenticated"
    assert res.status_code == 401

# DELTING POSTS
def test_unauth_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_auth_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts) - 1
 
def test_auth_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/9999")
    assert res.status_code == 404

def test_auth_delete_post_not_owner(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403

def test_auth_delete_post_admin(authorized_admin, test_user, test_posts):
    res = authorized_admin.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    res = authorized_admin.get("/posts/")
    assert len(res.json()) == len(test_posts) - 1

# UPDATING POSTS
def test_auth_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "goal": 777,
        "image": "UpdatedEncodedStr"
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    for attr in ['title', 'content', 'goal', 'image']:    
        assert getattr(updated_post, attr) == data[attr]
    assert res.status_code == 200

def test_unauth_update_post(client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "goal": 777,
        "image": "UpdatedEncodedStr"
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401

def test_auth_update_post_not_owner(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "goal": 777,
        "image": "UpdatedEncodedStr"
    }
    res = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 403

def test_auth_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "goal": 777,
        "image": "UpdatedEncodedStr"
    }
    res = authorized_client.put("/posts/9999", json=data)
    assert res.status_code == 404

def test_auth_update_post_admin(authorized_admin, test_user, test_posts):
    data = {
        "title": "Updated title",
        "content": "Updated content",
        "goal": 777,
        "image": "UpdatedEncodedStr"
    }
    res = authorized_admin.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    for attr in ['title', 'content', 'goal', 'image']:    
        assert getattr(updated_post, attr) == data[attr]
    assert res.status_code == 200

# MAKING PAYMENT
def test_auth_payment(authorized_client, test_user, test_posts, test_payments):
    post_id = test_posts[0].id
    res = authorized_client.post(f"/posts/{test_posts[0].id}/payment", json={
        "ammount": 50
    })
    new_payment = schemas.Payment(**res.json())
    assert new_payment.id == len(test_payments) + 1
    assert new_payment.ammount == 50
    assert new_payment.status == True
    assert new_payment.user_id == test_user["id"]
    assert res.status_code == 202

def test_unauth_payment(client, test_user, test_posts, test_payments):
    res = client.post(f"/posts/{test_posts[0].id}/payment", json={
        "ammount": 50
    })
    assert res.status_code == 401

