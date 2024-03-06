import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import models
from api.cocktail import cocktail_schema, cocktail_crud
from api.material import material_schema, material_crud
from api.spirit import spirit_schema, spirit_crud
from api.user import user_crud, user_schema
from db.database import Base, get_db
from main import app


class TestSession(Session):
    def commit(self) -> None:
        self.flush()


DB_URL = "/tests/test.db"
SQLALCHEMY_DATABASE_URL = "sqlite://" + DB_URL
# if not os.path.isfile(SQLALCHEMY_DATABASE_URL):
#     SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine, class_=TestSession)


@pytest.fixture(scope="session")
def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db(init_db):
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as _client:
        yield _client


@pytest.fixture(scope="function")
def cocktail(db):
    from tests.test_data import cocktail_data
    _cocktail = cocktail_crud.create_cocktail(db, cocktail_schema.CocktailCreate(**cocktail_data))

    cocktail_data = {
        "id": _cocktail.id,
        "name": _cocktail.name,
        "name_ko": _cocktail.name_ko,
        "skill": _cocktail.skill,
        "abv": _cocktail.abv
    }
    return models.Cocktail(**cocktail_data)


@pytest.fixture(scope="function")
def spirit(db):
    from tests.test_data import spirit_data
    _spirit = spirit_crud.create_spirit(db, spirit_schema.SpiritCreate(**spirit_data))

    spirit_data = {
        "id": _spirit.id,
        "type": _spirit.type,
        "name": _spirit.name,
        "name_ko": _spirit.name_ko,
        "unit": _spirit.unit,
        "amount": _spirit.amount,
        "cocktail_id": _spirit.cocktail_id
    }
    return models.Spirit(**spirit_data)


@pytest.fixture(scope="function")
def material(db):
    from tests.test_data import material_data
    _material = material_crud.create_material(db, material_schema.MaterialCreate(**material_data))

    material_data = {
        "id": _material.id,
        "type": _material.type,
        "name": _material.name,
        "name_ko": _material.name_ko,
        "unit": _material.unit,
        "amount": _material.amount,
        "cocktail_id": _material.cocktail_id
    }
    return models.Material(**material_data)


@pytest.fixture(scope="function")
def recipe(db):
    from tests.test_data import cocktail_data, spirit_data, material_data
    _cocktail = cocktail_crud.create_cocktail(db, cocktail_schema.CocktailCreate(**cocktail_data))
    spirit_data["cocktail_id"] = _cocktail.id
    material_data["cocktail_id"] = _cocktail.id

    _spirit = spirit_crud.create_spirit(db, spirit_schema.SpiritCreate(**spirit_data))
    _material = material_crud.create_material(db, material_schema.MaterialCreate(**material_data))

    recipe_data = {
        "id": _cocktail.id,
        "name": _cocktail.name,
        "name_ko": _cocktail.name_ko,
        "skill": _cocktail.skill,
        "abv": _cocktail.abv,
        "usage_count": 0,
        "spirits": [
            {
                "id": _spirit.id,
                "type": _spirit.type,
                "name": _spirit.name,
                "name_ko": _spirit.name_ko,
                "unit": _spirit.unit,
                "amount": _spirit.amount,
                "cocktail_id": _spirit.cocktail_id
            }
        ],
        "materials": [
            {
                "id": _material.id,
                "type": _material.type,
                "name": _material.name,
                "name_ko": _material.name_ko,
                "unit": _material.unit,
                "amount": _material.amount,
                "cocktail_id": _material.cocktail_id
            }
        ]

    }

    return cocktail_schema.CocktailDetail(**recipe_data)


@pytest.fixture(scope="function")
def user(db):
    from tests.test_data import user_data
    _user = user_crud.create_user(db, user_schema.UserCreate(**user_data))
    return _user


@pytest.fixture(scope="function")
def verified_user(db, user):
    _verified_user = user_crud.verified_email(db, user)
    return _verified_user


@pytest.fixture(scope="function")
def superuser(db, user):
    _superuser = user_crud.superuser(db, user)
    return _superuser


@pytest.fixture(scope="function")
def bookmark(db, verified_user, cocktail):
    from api.bookmark import bookmark_crud
    _bookmark = bookmark_crud.create_bookmark(db, verified_user, cocktail.id)
    return _bookmark
