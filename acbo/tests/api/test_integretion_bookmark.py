from tests.test_data import user_data


def test_bookmark_cocktail_list(client, verified_user, cocktail, bookmark):
    response = client.post("/api/users/login",
                           data={"username": verified_user.email, "password": user_data["password"]},
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
    res_user = response.json()
    assert response.status_code == 200

    response = client.get("/api/bookmarks",
                          headers={"Authorization": f"Bearer {res_user['access_token']}"})
    res = response.json()
    assert response.status_code == 200
    assert res['total'] == 1
    assert res['items'][0]['name'] == cocktail.name.replace("_", " ")
    assert res['items'][0]['name_ko'] == cocktail.name_ko.replace("_", " ")
    assert res['items'][0]['skill'] == cocktail.skill.value
    assert res['items'][0]['abv'] == cocktail.abv


def test_is_bookmarked(client, verified_user, cocktail, bookmark):
    response = client.post("/api/users/login",
                           data={"username": verified_user.email, "password": user_data["password"]},
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
    res_user = response.json()
    assert response.status_code == 200

    response = client.get(f"/api/bookmarks/{cocktail.id}",
                          headers={"Authorization": f"Bearer {res_user['access_token']}"})
    res = response.json()
    assert response.status_code == 200
    assert res['is_bookmarked'] is True

    response = client.get(f"/api/bookmarks/{cocktail.id+1}",
                          headers={"Authorization": f"Bearer {res_user['access_token']}"})
    res = response.json()
    assert response.status_code == 200
    assert res['is_bookmarked'] is False


def test_create_bookmark(client, verified_user, cocktail):
    response = client.post("/api/users/login",
                           data={"username": verified_user.email, "password": user_data["password"]},
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
    res_user = response.json()
    assert response.status_code == 200

    response = client.post(f"/api/bookmarks/{cocktail.id}",
                           headers={"Authorization": f"Bearer {res_user['access_token']}"})
    assert response.status_code == 201


def test_delete_bookmark(client, verified_user, cocktail, bookmark):
    response = client.post("/api/users/login",
                           data={"username": verified_user.email, "password": user_data["password"]},
                           headers={"Content-Type": "application/x-www-form-urlencoded"})
    res_user = response.json()
    assert response.status_code == 200

    response = client.delete(f"/api/bookmarks/{cocktail.id}",
                             headers={"Authorization": f"Bearer {res_user['access_token']}"})
    assert response.status_code == 204
