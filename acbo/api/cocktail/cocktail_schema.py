from typing import List

from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

from api.material.material_schema import Material, MaterialBase, MaterialRequest
from api.spirit.spirit_schema import Spirit, SpiritBase, SpiritRequest
from core.enums import Skill


class CocktailBase(BaseModel):
    name: str
    name_ko: str
    skill: Skill
    abv: int


class Cocktail(CocktailBase):
    id: int
    usage_count: int


class CocktailDetail(Cocktail):
    spirits: List[Spirit] = []
    materials: List[Material] = []


class CocktailList(BaseModel):
    total: int
    cocktails: List[Cocktail] = []


class CocktailSpirits(BaseModel):
    total: int
    spirits: List[Spirit] = []


class CocktailMaterials(BaseModel):
    total: int
    materials: List[Material] = []


class CocktailDetailByName(Cocktail):
    spirits: List[SpiritBase] = []
    materials: List[MaterialBase] = []


class CocktailListBySpiritMaterial(BaseModel):
    """
    Frontend 의 칵테일 탭
    """

    total: int
    items: List[CocktailBase] = []


class CocktailCreate(CocktailBase):
    @field_validator("name", "name_ko")
    def validate_cocktail(cls, v):
        if not v or not v.strip():
            raise PydanticCustomError(
                "ValueError", "빈 값은 허용되지 않습니다.", {"value": v}
            )
        return v

    @field_validator("skill")
    def skill_check(cls, v):
        if v.name not in Skill.__members__:
            raise ValueError("존재하지 않는 스킬입니다.")
        return v

    @field_validator("abv")
    def abv_check(cls, v):
        if type(v) is not int:
            raise ValueError("숫자만 입력해주세요.")
        elif v < 0:
            raise ValueError("0 미만의 숫자는 허용되지 않습니다.")
        return v


class CocktailUpdate(CocktailCreate):
    pass


class CocktailRequest(CocktailCreate):
    """
    GCS에 저장할 칵테일 레시피 JSON의 Cocktail
    """

    spirits: List[SpiritRequest] = []
    materials: List[MaterialRequest] = []
