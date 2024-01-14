from pydantic import BaseModel, field_validator

from api.material.material_schema import Material
from api.spirit.spirit_schema import Spirit
from models import Skill


class Cocktail(BaseModel):
    id: int
    name: str
    usage_count: int


class CocktailDetail(Cocktail):
    skill: Skill
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
    cocktails: list[CocktailDetail] = []


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


class CocktailBySpiritMaterial(BaseModel):
    total: int
    items: list[Cocktail] = []
    pass
