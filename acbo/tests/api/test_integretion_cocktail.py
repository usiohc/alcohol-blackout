def test_cocktail_list(client, cocktail):
    response = client.get("/api/cocktails")
    res = response.json()
    assert response.status_code == 200
    assert res['total'] == 1
    assert res['cocktails'][0]['id'] == cocktail.id
    assert res['cocktails'][0]['name'] == cocktail.name.replace("_", " ")
    assert res['cocktails'][0]['name_ko'] == cocktail.name_ko.replace("_", " ")
    assert res['cocktails'][0]['skill'] == cocktail.skill.value
    assert res['cocktails'][0]['abv'] == cocktail.abv


def test_cocktail_detail(client, cocktail):
    response = client.get(f"/api/cocktails/{cocktail.id}")
    res = response.json()
    assert response.status_code == 200
    assert res['id'] == cocktail.id
    assert res['name'] == cocktail.name.replace("_", " ")
    assert res['name_ko'] == cocktail.name_ko.replace("_", " ")
    assert res['skill'] == cocktail.skill.value
    assert res['abv'] == cocktail.abv
    assert res['spirits'] == []
    assert res['materials'] == []


def test_cocktail_spirit_list(client, recipe):
    response = client.get(f"/api/cocktails/{recipe.id}/spirits")
    res = response.json()
    assert response.status_code == 200
    assert res['total'] == 1
    assert res['spirits'][0]['id'] == recipe.spirits[0].id
    assert res['spirits'][0]['type'] == recipe.spirits[0].type.value
    assert res['spirits'][0]['name'] == recipe.spirits[0].name.replace("_", " ")
    assert res['spirits'][0]['name_ko'] == recipe.spirits[0].name_ko.replace("_", " ")
    assert res['spirits'][0]['unit'] == recipe.spirits[0].unit.value
    assert res['spirits'][0]['amount'] == recipe.spirits[0].amount
    assert res['spirits'][0]['cocktail_id'] == recipe.spirits[0].cocktail_id


def test_cocktail_material_list(client, recipe):
    response = client.get(f"/api/cocktails/{recipe.id}/materials")
    res = response.json()
    assert response.status_code == 200
    assert res['total'] == 1
    assert res['materials'][0]['id'] == recipe.materials[0].id
    assert res['materials'][0]['type'] == recipe.materials[0].type.value
    assert res['materials'][0]['name'] == recipe.materials[0].name.replace("_", " ")
    assert res['materials'][0]['name_ko'] == recipe.materials[0].name_ko.replace("_", " ")
    assert res['materials'][0]['unit'] == recipe.materials[0].unit.value
    assert res['materials'][0]['amount'] == recipe.materials[0].amount
    assert res['materials'][0]['cocktail_id'] == recipe.materials[0].cocktail_id


def test_cocktail_create(client):
    cocktail_data = {
        "name": "Test Cocktail",
        "name_ko": "테스트 칵테일",
        "skill": "Float",
        "abv": 15
    }
    response = client.post("/api/cocktails", json=cocktail_data)
    assert response.status_code == 201
    assert response.json() is None


def test_cocktail_update(client, cocktail):
    updated_data = {
        "name": "Updated Cocktail",
        "name_ko": "업데이트된 칵테일",
        "skill": "Build",
        "abv": 10
    }
    response = client.put(f"/api/cocktails/{cocktail.id}", json=updated_data)
    assert response.status_code == 200
    assert response.json() is None


def test_cocktail_delete(client, cocktail):
    response = client.delete(f"/api/cocktails/{cocktail.id}")
    assert response.status_code == 204


def test_cocktail_spirit_material(client, recipe):
    # ?spirits=whisky&materials=Syrup:Simple
    s, m = f"{recipe.spirits[0].type.value}", f"{recipe.materials[0].type.value}:{recipe.materials[0].name.replace('_', ' ')}"
    tests = [
        f"/api/cocktails/?spirits={s}&materials={m}",
        f"/api/cocktails/?spirits=&materials={m}",
        f"/api/cocktails/?spirits={s}&materials=",
        f"/api/cocktails/?spirits=&materials=",
    ]
    for test in tests:
        response = client.get(test)
        res = response.json()
        assert response.status_code == 200
        assert res['total'] == 1
        assert res['items'][0]['name'] == recipe.name.replace("_", " ")
        assert res['items'][0]['name_ko'] == recipe.name_ko.replace("_", " ")
        assert res['items'][0]['skill'] == recipe.skill.value
        assert res['items'][0]['abv'] == recipe.abv
