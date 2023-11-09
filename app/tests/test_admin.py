import pytest
from app import schemas

# GETTING POSTS
def test_auth_get_admin_posts(authorized_admin, test_posts, test_user):
    res = authorized_admin.get("/admin/posts/")
    
    def validate(post):
        return schemas.AdminPost(**post)
    post_map = map(validate, res.json())
    posts_list = list(post_map)

    for post, test_post in zip(posts_list, test_posts):
        for attr in ['id', 'title', 'owner_id', 'created_at']:
            assert getattr(post, attr) == getattr(test_post, attr)
    assert res.status_code == 200

def test_unauth_get_admin_posts(client, test_posts, test_user):
    res = client.get("/admin/posts/")
    assert res.status_code == 401

# GETTING USERS
def test_auth_get_admin_users(authorized_admin, test_admin, test_user, test_user2):
    res = authorized_admin.get("/admin/users/")
    def validate(user):
        return schemas.AdminUser(**user)
    user_map = map(validate, res.json())
    user_list = list(user_map)

    # List of test users
    test_users = [test_admin, test_user, test_user2]
    # Excluding first element of user_list
    for i, user in enumerate(user_list):
        test_obj = test_users[i]
        for attr in ['id', 'name', 'email', 'created_at', 'privileged']:
            if attr == 'created_at' and test_obj != test_admin:
                # Date needs to be formatted from datetime.datetime to str
                date = user.created_at
                formatted_date = date.strftime('%Y-%m-%dT%H:%M:%S.%f')
                assert formatted_date == test_obj[attr]
            else:
                assert getattr(user, attr) == test_obj[attr]

    assert res.status_code == 200

def test_unauth_get_admin_users(client, test_posts, test_user):
    res = client.get("/admin/users/")
    assert res.status_code == 401

def test_auth_delete_admin_users(authorized_admin, test_posts, test_user):
    res = authorized_admin.delete(f"/admin/users/{test_user['id']}")
    assert res.status_code == 204
    res = authorized_admin.get("/admin/users/")
    assert len(res.json()) == len(test_posts) - 1

def test_auth_delete_admin_users_not_exist(authorized_admin, test_posts, test_user):
    res = authorized_admin.delete("/admin/users/9999")
    assert res.status_code == 404

def test_unauth_delete_admin_users(client, test_posts, test_user):
    res = client.delete(f"/admin/users/{test_user['id']}")
    assert res.status_code == 401