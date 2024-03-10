from api.spirit import spirit_crud, spirit_schema
from core.enums import SpiritType, Unit


def test_get_spirit_list(db, spirit):
    """
    - get_spirit_list() 함수 테스트
    - event listen 함수를 통해 name, name_ko에 대한 자동 변환 테스트
    """
    total, spirit_list = spirit_crud.get_spirit_list(db)
    assert total == 1
    assert spirit_list[0].id == spirit.id
    assert spirit_list[0].type == spirit.type
    assert spirit_list[0].name == spirit.name.replace("_", " ")
    assert spirit_list[0].name_ko == spirit.name_ko.replace("_", " ")
    assert spirit_list[0].unit == spirit.unit
    assert spirit_list[0].amount == spirit.amount
    assert spirit_list[0].cocktail_id == spirit.cocktail_id


def test_get_spirit(db, spirit):
    """
    - get_spirit() 함수 테스트
    - event listen 함수를 통해 name, name_ko에 대한 자동 변환 테스트
    """
    get_spirit = spirit_crud.get_spirit(db, spirit.id)
    assert get_spirit.id == spirit.id
    assert get_spirit.type == spirit.type
    assert get_spirit.name == spirit.name.replace("_", " ")
    assert get_spirit.name_ko == spirit.name_ko.replace("_", " ")
    assert get_spirit.unit == spirit.unit
    assert get_spirit.amount == spirit.amount
    assert get_spirit.cocktail_id == spirit.cocktail_id


def test_create_spirit(db):
    """
    - create_spirit() 함수 테스트
    - event listen 함수를 통해 name, name_ko에 대한 자동 변환 테스트
    """
    spirit_data = {
        "type": SpiritType.Whisky,
        "name": "Test Whisky",
        "name_ko": "테스트 위스키",
        "unit": Unit.ml,
        "amount": 50,
        "cocktail_id": None,
    }
    created_spirit = spirit_crud.create_spirit(
        db, spirit_schema.SpiritCreate(**spirit_data)
    )

    assert created_spirit.id == 1
    assert created_spirit.type == spirit_data["type"]
    assert created_spirit.name == spirit_data["name"].replace(" ", "_")
    assert created_spirit.name_ko == spirit_data["name_ko"].replace(" ", "_")
    assert created_spirit.unit == spirit_data["unit"]
    assert created_spirit.amount == spirit_data["amount"]
    assert created_spirit.cocktail_id == spirit_data["cocktail_id"]


def test_update_spirit(db, spirit):
    """
    - update_spirit() 함수 테스트
    - event listen 함수를 통해 name, name_ko에 대한 자동 변환 테스트
    """
    spirit_data = {
        "type": SpiritType.Gin,
        "name": "Updated Gin",
        "name_ko": "업데이트된 Gin",
        "unit": Unit.ml,
        "amount": 60,
        "cocktail_id": None,
    }
    spirit = spirit_crud.get_spirit(db, spirit.id)
    updated_spirit = spirit_crud.update_spirit(
        db, spirit, spirit_schema.SpiritUpdate(**spirit_data)
    )
    assert updated_spirit.id == spirit.id
    assert updated_spirit.type == spirit_data["type"]
    assert updated_spirit.name == spirit_data["name"].replace(" ", "_")
    assert updated_spirit.name_ko == spirit_data["name_ko"].replace(" ", "_")
    assert updated_spirit.unit == spirit_data["unit"]
    assert updated_spirit.amount == spirit_data["amount"]
    assert updated_spirit.cocktail_id == spirit_data["cocktail_id"]


def test_delete_spirit(db, spirit):
    spirit_crud.delete_spirit(db, spirit.id)
    assert spirit_crud.get_spirit(db, spirit.id) is None
