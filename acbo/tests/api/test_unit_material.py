from api.material import material_crud, material_schema
from enums import MaterialType, Unit


def test_get_material_list(db, material):
    """
    - get_material_list() 함수 테스트
    """
    total, material_list = material_crud.get_material_list(db)
    assert total == 1
    assert material_list[0].id == material.id
    assert material_list[0].type == material.type
    assert material_list[0].name == material.name.replace("_", " ")
    assert material_list[0].name_ko == material.name_ko.replace("_", " ")
    assert material_list[0].unit == material.unit
    assert material_list[0].amount == material.amount
    assert material_list[0].cocktail_id == material.cocktail_id


def test_get_material(db, material):
    """
    - get_material() 함수 테스트
    """
    get_material = material_crud.get_material(db, material.id)
    assert get_material.id == material.id
    assert get_material.type == material.type
    assert get_material.name == material.name.replace("_", " ")
    assert get_material.name_ko == material.name_ko.replace("_", " ")
    assert get_material.unit == material.unit
    assert get_material.amount == material.amount
    assert get_material.cocktail_id == material.cocktail_id


def test_create_material(db):
    """
    - create_material() 함수 테스트
    """
    material_data = {
        "type": MaterialType.Liqueur,
        "name": "Test Liqueur",
        "name_ko": "테스트 리큐어",
        "unit": Unit.ml,
        "amount": 50,
        "cocktail_id": None
    }
    created_material = material_crud.create_material(db, material_schema.MaterialCreate(**material_data))
    assert created_material.id == 1
    assert created_material.type == material_data["type"]
    assert created_material.name == material_data["name"].replace(" ", "_")
    assert created_material.name_ko == material_data["name_ko"].replace(" ", "_")
    assert created_material.unit == material_data["unit"]
    assert created_material.amount == material_data["amount"]
    assert created_material.cocktail_id == material_data["cocktail_id"]


def test_update_material(db, material):
    """
    - update_material() 함수 테스트
    """
    material_data = {
        "type": MaterialType.Syrup,
        "name": "Updated Material",
        "name_ko": "업데이트된 시럽",
        "unit": Unit.ml,
        "amount": 60,
        "cocktail_id": None
    }
    material = material_crud.get_material(db, material.id)
    updated_material = material_crud.update_material(db, material, material_schema.MaterialUpdate(**material_data))
    assert updated_material.id == material.id
    assert updated_material.type == material_data["type"]
    assert updated_material.name == material_data["name"].replace(" ", "_")
    assert updated_material.name_ko == material_data["name_ko"].replace(" ", "_")
    assert updated_material.unit == material_data["unit"]
    assert updated_material.amount == material_data["amount"]
    assert updated_material.cocktail_id == material_data["cocktail_id"]


def test_delete_material(db, material):
    """
    - delete_material() 함수 테스트
    """
    material_crud.delete_material(db, material.id)
    assert material_crud.get_material(db, material.id) is None


def test_get_material_by_spirit(db, recipe):
    """
    - get_material_list_by_cocktail() 함수 테스트
    """
    spirits = []
    total, material_list = material_crud.get_material_by_spirit(db, spirits)
    assert total == 1
    assert material_list[0].type == recipe.materials[0].type
    assert material_list[0].name == recipe.materials[0].name.replace("_", " ")
    assert material_list[0].name_ko == recipe.materials[0].name_ko.replace("_", " ")

    spirits = list(map(lambda x: x.type.value, recipe.spirits))
    total, material_list = material_crud.get_material_by_spirit(db, spirits)
    assert total == 1
    assert material_list[0].type == recipe.materials[0].type
    assert material_list[0].name == recipe.materials[0].name.replace("_", " ")
    assert material_list[0].name_ko == recipe.materials[0].name_ko.replace("_", " ")
