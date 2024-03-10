from core.enums import MaterialType, Skill, SpiritType, Unit

cocktail_data = {
    "name": "Test Cocktail",
    "name_ko": "테스트 칵테일",
    "skill": Skill.Stir,
    "abv": 10,
}

spirit_data = {
    "type": SpiritType.Whisky,
    "name": "Test Spirit",
    "name_ko": "테스트 기주",
    "unit": Unit.ml,
    "amount": 50,
    "cocktail_id": None,
}

material_data = {
    "type": MaterialType.Syrup,
    "name": "Test Material",
    "name_ko": "테스트 재료",
    "unit": Unit.ml,
    "amount": 50,
    "cocktail_id": None,
}

user_data = {
    "username": "test_user",
    "email": "test_user@test.com",
    "password": "test_password",
    "passwordCheck": "test_password",
}

email_token_data = {"token": "test_token", "email": user_data["email"]}
