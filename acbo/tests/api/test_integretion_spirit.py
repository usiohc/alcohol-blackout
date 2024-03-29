from tests.test_data import user_data


def test_spirit_list(client, spirit):
    response = client.get("/api/spirits")
    res = response.json()
    assert response.status_code == 200
    assert res["total"] == 1
    assert res["spirits"][0]["id"] == spirit.id
    assert res["spirits"][0]["type"] == spirit.type.value
    assert res["spirits"][0]["name"] == spirit.name.replace("_", " ")
    assert res["spirits"][0]["name_ko"] == spirit.name_ko.replace("_", " ")
    assert res["spirits"][0]["unit"] == spirit.unit.value
    assert res["spirits"][0]["amount"] == spirit.amount
    assert res["spirits"][0]["cocktail_id"] == spirit.cocktail_id


def test_spirit_detail(client, spirit):
    response = client.get(f"/api/spirits/{spirit.id}")
    res = response.json()
    assert response.status_code == 200
    assert res["id"] == spirit.id
    assert res["type"] == spirit.type.value
    assert res["name"] == spirit.name.replace("_", " ")
    assert res["name_ko"] == spirit.name_ko.replace("_", " ")
    assert res["unit"] == spirit.unit.value
    assert res["amount"] == spirit.amount
    assert res["cocktail_id"] == spirit.cocktail_id


def test_spirit_create(client, superuser):
    response = client.post(
        "/api/users/login",
        data={"username": superuser.email, "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    _superuser = response.json()
    assert response.status_code == 200
    assert _superuser["access_token"] is not None

    spirit_data = {
        "type": "Whisky",
        "name": "Test Whiskey",
        "name_ko": "테스트 위스키",
        "unit": "ml",
        "amount": 50,
        "cocktail_id": None,
    }
    response = client.post(
        "/api/spirits",
        json=spirit_data,
        headers={"Authorization": f"Bearer {_superuser['access_token']}"},
    )
    res = response.json()
    assert response.status_code == 201
    assert res["id"] is not None
    assert res["type"] == spirit_data["type"]
    assert res["name"] == spirit_data["name"].replace(" ", "_")
    assert res["name_ko"] == spirit_data["name_ko"].replace(" ", "_")
    assert res["unit"] == spirit_data["unit"]
    assert res["amount"] == spirit_data["amount"]
    assert res["cocktail_id"] == spirit_data["cocktail_id"]


def test_spirit_update(client, spirit, superuser):
    response = client.post(
        "/api/users/login",
        data={"username": superuser.email, "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    _superuser = response.json()
    assert response.status_code == 200
    assert _superuser["access_token"] is not None

    updated_data = {
        "type": "Gin",
        "name": "Updated Gin",
        "name_ko": "업데이트된 진",
        "unit": "ml",
        "amount": 60,
        "cocktail_id": None,
    }
    response = client.put(
        f"/api/spirits/{spirit.id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {_superuser['access_token']}"},
    )
    res = response.json()
    assert response.status_code == 200
    assert res["id"] is not None
    assert res["type"] == updated_data["type"]
    assert res["name"] == updated_data["name"].replace(" ", "_")
    assert res["name_ko"] == updated_data["name_ko"].replace(" ", "_")
    assert res["unit"] == updated_data["unit"]
    assert res["amount"] == updated_data["amount"]
    assert res["cocktail_id"] == updated_data["cocktail_id"]


def test_spirit_delete(client, spirit, superuser):
    response = client.post(
        "/api/users/login",
        data={"username": superuser.email, "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    _superuser = response.json()
    assert response.status_code == 200
    assert _superuser["access_token"] is not None

    response = client.delete(
        f"/api/spirits/{spirit.id}",
        headers={"Authorization": f"Bearer {_superuser['access_token']}"},
    )
    assert response.status_code == 204
