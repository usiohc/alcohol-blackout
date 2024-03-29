from tests.test_data import user_data


def test_material_list(client, material):
    response = client.get("/api/materials")
    res = response.json()
    assert response.status_code == 200
    assert res["total"] == 1
    assert res["materials"][0]["id"] == material.id
    assert res["materials"][0]["type"] == material.type.value
    assert res["materials"][0]["name"] == material.name.replace("_", " ")
    assert res["materials"][0]["name_ko"] == material.name_ko.replace("_", " ")
    assert res["materials"][0]["unit"] == material.unit.value
    assert res["materials"][0]["amount"] == material.amount


def test_material_detail(client, material):
    response = client.get(f"/api/materials/{material.id}")
    res = response.json()
    assert response.status_code == 200
    assert res["id"] == material.id
    assert res["type"] == material.type.value
    assert res["name"] == material.name.replace("_", " ")
    assert res["name_ko"] == material.name_ko.replace("_", " ")
    assert res["unit"] == material.unit.value
    assert res["amount"] == material.amount
    assert res["cocktail_id"] == material.cocktail_id


def test_material_create(client, superuser):
    response = client.post(
        "/api/users/login",
        data={"username": superuser.email, "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    _superuser = response.json()
    assert response.status_code == 200
    assert _superuser["access_token"] is not None

    material_data = {
        "type": "Liqueur",
        "name": "Test Liqueur",
        "name_ko": "테스트 리큐어",
        "unit": "ml",
        "amount": 10,
        "cocktail_id": None,
    }
    response = client.post(
        "/api/materials",
        json=material_data,
        headers={"Authorization": f"Bearer {_superuser['access_token']}"},
    )
    res = response.json()
    assert response.status_code == 201
    assert res["id"] is not None
    assert res["type"] == material_data["type"]
    assert res["name"] == material_data["name"].replace(" ", "_")
    assert res["name_ko"] == material_data["name_ko"].replace(" ", "_")
    assert res["unit"] == material_data["unit"]
    assert res["amount"] == material_data["amount"]
    assert res["cocktail_id"] == material_data["cocktail_id"]


def test_material_update(client, material, superuser):
    response = client.post(
        "/api/users/login",
        data={"username": superuser.email, "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    _superuser = response.json()
    assert response.status_code == 200
    assert _superuser["access_token"] is not None

    updated_data = {
        "type": "Juice",
        "name": "Updated Juice",
        "name_ko": "업데이트된 주스",
        "unit": "ml",
        "amount": 40,
        "cocktail_id": None,
    }
    response = client.put(
        f"/api/materials/{material.id}",
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


def test_material_delete(client, material, superuser):
    response = client.post(
        "/api/users/login",
        data={"username": superuser.email, "password": user_data["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    _superuser = response.json()
    assert response.status_code == 200
    assert _superuser["access_token"] is not None

    response = client.delete(
        f"/api/materials/{material.id}",
        headers={"Authorization": f"Bearer {_superuser['access_token']}"},
    )
    assert response.status_code == 204


def test_material_by_spirit(client, recipe):
    response = client.get("/api/materials/?spirits=")
    res = response.json()
    assert response.status_code == 200
    assert res["total"] == 1
    assert res["items"][0]["type"] == recipe.materials[0].type.value
    assert res["items"][0]["name"] == recipe.materials[0].name.replace("_", " ")
    assert res["items"][0]["name_ko"] == recipe.materials[0].name_ko.replace("_", " ")

    spirits = ",".join(map(lambda x: x.type.value, recipe.spirits))
    response = client.get(f"/api/materials/?spirits={spirits}")
    res = response.json()
    assert response.status_code == 200
    assert res["total"] == 1
    assert res["items"][0]["type"] == recipe.materials[0].type.value
    assert res["items"][0]["name"] == recipe.materials[0].name.replace("_", " ")
    assert res["items"][0]["name_ko"] == recipe.materials[0].name_ko.replace("_", " ")
