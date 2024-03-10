from api.cocktail import cocktail_crud, cocktail_schema
from core.enums import Skill


def test_cocktail_list(db, cocktail):
    total, cocktail_list = cocktail_crud.get_cocktail_list(db)
    assert total == 1
    assert cocktail_list[0].id == cocktail.id
    assert cocktail_list[0].name == cocktail.name.replace("_", " ")
    assert cocktail_list[0].name_ko == cocktail.name_ko.replace("_", " ")
    assert cocktail_list[0].skill == cocktail.skill
    assert cocktail_list[0].abv == cocktail.abv


def test_cocktail_detail(db, cocktail):
    get_cocktail = cocktail_crud.get_cocktail(db, cocktail.id)
    assert get_cocktail.id == cocktail.id
    assert get_cocktail.name == cocktail.name.replace("_", " ")
    assert get_cocktail.name_ko == cocktail.name_ko.replace("_", " ")
    assert get_cocktail.skill == cocktail.skill
    assert get_cocktail.abv == cocktail.abv


def test_cocktail_spirit_material(db, recipe):
    spirit_total, spirit_list = cocktail_crud.get_cocktail_spirit_list(db, recipe.id)
    material_total, material_list = cocktail_crud.get_cocktail_material_list(
        db, recipe.id
    )

    assert spirit_total == 1
    assert spirit_list[0].id == recipe.spirits[0].id
    assert spirit_list[0].type == recipe.spirits[0].type
    assert spirit_list[0].name == recipe.spirits[0].name.replace("_", " ")
    assert spirit_list[0].name_ko == recipe.spirits[0].name_ko.replace("_", " ")
    assert spirit_list[0].unit == recipe.spirits[0].unit
    assert spirit_list[0].amount == recipe.spirits[0].amount
    assert spirit_list[0].cocktail_id == recipe.spirits[0].cocktail_id

    assert material_total == 1
    assert material_list[0].id == recipe.materials[0].id
    assert material_list[0].type == recipe.materials[0].type
    assert material_list[0].name == recipe.materials[0].name.replace("_", " ")
    assert material_list[0].name_ko == recipe.materials[0].name_ko.replace("_", " ")
    assert material_list[0].unit == recipe.materials[0].unit
    assert material_list[0].amount == recipe.materials[0].amount
    assert material_list[0].cocktail_id == recipe.materials[0].cocktail_id


def test_cocktail_create(db):
    cocktail_data = {
        "name": "Test Cocktail",
        "name_ko": "테스트 칵테일",
        "skill": Skill.Shake,
        "abv": 5,
    }
    created_cocktail = cocktail_crud.create_cocktail(
        db, cocktail_schema.CocktailCreate(**cocktail_data)
    )
    assert created_cocktail.id == 1
    assert created_cocktail.name == cocktail_data["name"].replace(" ", "_")
    assert created_cocktail.name_ko == cocktail_data["name_ko"].replace(" ", "_")
    assert created_cocktail.skill == cocktail_data["skill"]
    assert created_cocktail.abv == cocktail_data["abv"]


def test_cocktail_update(db, cocktail):
    updated_data = {
        "name": "Updated Cocktail",
        "name_ko": "업데이트된 칵테일",
        "skill": Skill.Float,
        "abv": 20,
    }
    cocktail = cocktail_crud.get_cocktail(db, cocktail.id)
    updated_cocktail = cocktail_crud.update_cocktail(
        db, cocktail, cocktail_schema.CocktailUpdate(**updated_data)
    )
    assert updated_cocktail.id == cocktail.id
    assert updated_cocktail.name == updated_data["name"].replace(" ", "_")
    assert updated_cocktail.name_ko == updated_data["name_ko"].replace(" ", "_")
    assert updated_cocktail.skill == updated_data["skill"]
    assert updated_cocktail.abv == updated_data["abv"]


def test_cocktail_delete(db, cocktail):
    cocktail_crud.delete_cocktail(db, cocktail.id)
    assert cocktail_crud.get_cocktail(db, cocktail.id) is None


def test_cocktail_by_spirit_material(db, recipe):
    s, m = list(map(lambda x: x.type.value, recipe.spirits)), list(
        map(lambda x: [x.type.value, x.name], recipe.materials)
    )
    tests = [
        (s, m),
        (s, []),
        ([], m),
        ([], []),
    ]
    for spirits, materials in tests:
        total, cocktail_list = cocktail_crud.get_cocktail_by_spirit_material(
            db, spirits, materials
        )
        assert total == 1
        assert cocktail_list[0].id == recipe.id
        assert cocktail_list[0].name == recipe.name.replace("_", " ")
        assert cocktail_list[0].name_ko == recipe.name_ko.replace("_", " ")
        assert cocktail_list[0].skill == recipe.skill
        assert cocktail_list[0].abv == recipe.abv


def test_cocktail_detail_by_name(db, cocktail):
    get_cocktail = cocktail_crud.get_cocktail_detail_by_name(db, cocktail.name)
    assert get_cocktail.name == cocktail.name.replace("_", " ")
    assert get_cocktail.name_ko == cocktail.name_ko.replace("_", " ")
    assert get_cocktail.skill == cocktail.skill
    assert get_cocktail.abv == cocktail.abv
