import pytest

def test_register_user(test_client):
    user_data = {
        "email": "newuser@example.com",
        "password_hash": "newpassword"
    }
    response = test_client.post("/user/register", json=user_data)

    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]

def test_register_existing_user(test_client, test_user):
    user_data = {
        "email": test_user["user_email"],
        "password_hash": "anotherpassword"
    }
    response = test_client.post("/user/register", json=user_data)

    assert response.status_code == 400
    assert response.json()["detail"] == f"User with email {test_user['user_email']} already exists"

def test_login_success(test_client, test_user):
    login_data = {
        "email": test_user["user_email"],
        "password": test_user["plain_password"]
    }
    response = test_client.post("/user/login", json=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["user"]["email"] == test_user["user_email"]

def test_login_invalid_user(test_client):
    login_data = {
        "email": "unknownuser@example.com",
        "password": "password"
    }
    response = test_client.post("/user/login", json=login_data)

    assert response.status_code == 400
    assert response.json()["detail"] == "401: Sorry, there was a problem, the login failed"

def test_login_invalid_password(test_client, test_user):
    login_data = {
        "email": test_user["user_email"],
        "password": "wrongpassword"
    }
    response = test_client.post("/user/login", json=login_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "401: Sorry, there was a problem, the login failed"

def test_authenticated_user_endpoint(test_client, auth_headers):
    response = test_client.get("/user/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "User is authenticated"

def test_user_not_authenticated(test_client):
    response = test_client.get("/user/")
    assert response.status_code == 401
    assert response.json()["detail"] == "401: Token not found"
