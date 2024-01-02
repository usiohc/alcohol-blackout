from pydantic import BaseModel, field_validator

from api.material.material_schema import Material
from api.spirit.spirit_schema import Spirit


class Cocktail(BaseModel):
    id: int
    name: str
    usage_count: int
    spirits: list[Spirit] = []
    materials: list[Material] = []


class CocktailSpiritList(BaseModel):
    total: int
    spirits: list[Spirit] = []


class CocktailMaterialList(BaseModel):
    total: int
    materials: list[Material] = []


class CocktailList(BaseModel):
    total: int
    cocktails: list[Cocktail] = []


class CocktailCreate(BaseModel):
    name: str
    usage_count: int = 0

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) > 20:
            raise ValueError('칵테일 이름은 20자 이하로 입력해주세요.')
        return v


class CocktailUpdate(CocktailCreate):
    pass
