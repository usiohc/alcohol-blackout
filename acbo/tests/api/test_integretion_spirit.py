def test_spirit_list(client, spirit):
    response = client.get("/api/spirits")
    res = response.json()
    assert response.status_code == 200
    assert res['total'] == 1
    assert res['spirits'][0]['id'] == spirit.id
    assert res['spirits'][0]['type'] == spirit.type.value
    assert res['spirits'][0]['name'] == spirit.name.replace("_", " ")
    assert res['spirits'][0]['name_ko'] == spirit.name_ko.replace("_", " ")
    assert res['spirits'][0]['unit'] == spirit.unit.value
    assert res['spirits'][0]['amount'] == spirit.amount
    assert res['spirits'][0]['cocktail_id'] == spirit.cocktail_id


def test_spirit_detail(client, spirit):
    response = client.get(f"/api/spirits/{spirit.id}")
    res = response.json()
    assert response.status_code == 200
    assert res['id'] == spirit.id
    assert res['type'] == spirit.type.value
    assert res['name'] == spirit.name.replace("_", " ")
    assert res['name_ko'] == spirit.name_ko.replace("_", " ")
    assert res['unit'] == spirit.unit.value
    assert res['amount'] == spirit.amount
    assert res['cocktail_id'] == spirit.cocktail_id


def test_spirit_create(client):
    spirit_data = {
        "type": "Whisky",
        "name": "Test Whiskey",
        "name_ko": "테스트 위스키",
        "unit": "ml",
        "amount": 50,
        "cocktail_id": None
    }
    response = client.post("/api/spirits", json=spirit_data)
    assert response.status_code == 201
    assert response.json() is None


def test_spirit_update(client, spirit):
    updated_data = {
        "type": "Gin",
        "name": "Updated Gin",
        "name_ko": "업데이트된 진",
        "unit": "ml",
        "amount": 60,
        "cocktail_id": None
    }
    response = client.put(f"/api/spirits/{spirit.id}", json=updated_data)
    assert response.status_code == 200
    assert response.json() is None


def test_spirit_delete(client, spirit):
    response = client.delete(f"/api/spirits/{spirit.id}")
    assert response.status_code == 204
