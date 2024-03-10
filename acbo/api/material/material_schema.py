from typing import List, Optional

from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

from core.enums import MaterialType, Unit


class MaterialBase(BaseModel):
    type: MaterialType
    name: str
    name_ko: str
    unit: Unit
    amount: int


class Material(MaterialBase):
    id: int
    cocktail_id: Optional[int]


class MaterialList(BaseModel):
    total: int
    materials: List[Material] = []


class MaterialOmittedUnitAmount(BaseModel):
    type: MaterialType
    name: str
    name_ko: str


class MaterialListBySpirit(BaseModel):
    """
    Frontend 의 재료 탭
    """

    total: int
    items: List[MaterialOmittedUnitAmount] = []


class MaterialBaseCreate(MaterialBase):
    @field_validator("name", "name_ko")
    def validate_material(cls, v):
        if not v or not v.strip():
            raise PydanticCustomError(
                "ValueError", "빈 값은 허용되지 않습니다.", {"value": v}
            )
        return v

    @field_validator("type")
    def validate_material_type(cls, v):
        if v.name not in MaterialType.__members__:
            raise ValueError("존재하지 않는 재료 입니다.")
        return v

    @field_validator("unit")
    def unit_check(cls, v):
        if v.name not in Unit.__members__:
            raise ValueError("존재하지 않는 단위 입니다.")
        return v

    @field_validator("amount")
    def amount_check(cls, v, values):
        if type(v) is not int:
            raise ValueError("숫자만 입력해주세요.")
        elif v <= 0 and values.data["unit"].name != "Full_up":
            raise ValueError("0 이하의 숫자는 허용되지 않습니다.")
        return v


class MaterialCreate(MaterialBaseCreate):
    cocktail_id: Optional[int]


class MaterialUpdate(MaterialCreate):
    pass


class MaterialRequest(MaterialBaseCreate):
    """
    GCS에 저장할 칵테일 레시피 JSON의 Material
    """

    pass
