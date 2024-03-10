from api.user.email.email import fm
from api.user.user_router import make_access_token
from tests.test_data import user_data


def test_user_register(client):
    fm.config.SUPPRESS_SEND = 1  # 실제 전송 X
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    access_token = make_access_token(user_data["email"], 1)
    response = client.post("/api/oauth2/token", json={"token": access_token})
    print(response.json())
    assert response.status_code == 200


def test_user_login_me_update(client, verified_user):
    response = client.post(
        "/api/users/login",
        data={"username": verified_user.email, "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    res = response.json()
    assert response.status_code == 200
    assert res["access_token"] is not None
    assert res["token_type"] == "bearer"
    assert res["email"] == verified_user.email
    assert res["username"] == verified_user.username

    response = client.patch(
        "/api/users/username",
        json={"username": "new_username"},
        headers={"Authorization": f"Bearer {res['access_token']}"},
    )
    assert response.status_code == 200

    response = client.patch(
        "/api/users/password",
        json={"password": "new_password", "passwordCheck": "new_password"},
        headers={"Authorization": f"Bearer {res['access_token']}"},
    )
    assert response.status_code == 200

    response = client.get(
        "/api/users/me", headers={"Authorization": f"Bearer {res['access_token']}"}
    )
    res = response.json()
    assert response.status_code == 200
    assert res["email"] == verified_user.email
    assert res["username"] == verified_user.username


def test_user_delete(client, verified_user):
    response = client.post(
        "/api/users/login",
        data={"username": verified_user.email, "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    res = response.json()
    assert response.status_code == 200

    response = client.delete(
        "/api/users", headers={"Authorization": f"Bearer {res['access_token']}"}
    )
    assert response.status_code == 200
