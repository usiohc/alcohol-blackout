from pydantic import BaseModel, field_validator

from api.material.material_schema import Material, MaterialRequest
from api.spirit.spirit_schema import Spirit, SpiritRequest
from models import Skill


class Cocktail(BaseModel):
    id: int
    name: str
    name_ko: str
    skill: Skill
    abv: int
    usage_count: int


class CocktailDetail(Cocktail):
    spirits: list[Spirit] = []
    materials: list[Material] = []


class CocktailList(BaseModel):
    total: int
    cocktails: list[CocktailDetail] = []


class CocktailSpiritList(BaseModel):
    total: int
    spirits: list[Spirit] = []


class CocktailMaterialList(BaseModel):
    total: int
    materials: list[Material] = []


class CocktailCreate(BaseModel):
    name: str
    name_ko: str
    skill: Skill
    abv: int

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) > 50:
            raise ValueError('칵테일 이름은 20자 이하로 입력해주세요.')
        return v


class CocktailUpdate(CocktailCreate):
    pass


class CocktailBySpiritMaterial(BaseModel):
    total: int
    items: list[Cocktail] = []


class CocktailRequest(BaseModel):
    """
    GCS에 저장할 칵테일 레시피 JSON의 Cocktail
    """
    name: str
    name_ko: str
    skill: Skill
    abv: int
    spirits: list[SpiritRequest] = []
    materials: list[MaterialRequest] = []
