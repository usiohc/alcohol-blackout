from pydantic import BaseModel, field_validator, Field
from pydantic_core import PydanticCustomError

from models import MaterialType, Unit


class Material(BaseModel):
    id: int
    type: MaterialType
    name: str
    name_ko: str
    unit: Unit
    amount: int
    cocktail_id: int


class MaterialList(BaseModel):
    total: int
    materials: list[Material] = []


class MaterialCreate(BaseModel):
    type: MaterialType
    name: str
    name_ko: str
    unit: Unit
    amount: int
    cocktail_id: int


    @field_validator('type', 'name', 'name_ko', 'unit', 'amount')
    def validate_material(cls, v):
        if not v or not v.strip():
            raise PydanticCustomError("ValueError",
                                      "빈 값은 허용되지 않습니다.",
                                      {"value": v})
        return v

    @field_validator('type')
    def validate_material_type(cls, v):
        if v.name not in MaterialType.__members__:
            raise ValueError('존재하지 않는 재료 입니다.')
        return v

    @field_validator('unit')
    def unit_check(cls, v):
        if v.name not in Unit.__members__:
            raise ValueError('존재하지 않는 단위 입니다.')
        return v

    @field_validator('amount')
    def amount_check(cls, v, values):
        if type(v) is not int:
            raise ValueError('숫자만 입력해주세요.')
        elif v <= 0 and values.data['unit'].name != 'Full_up':
            raise ValueError('0 이하의 숫자는 허용되지 않습니다.')
        return v


class MaterialUpdate(MaterialCreate):
    pass


class MaterialBySpirit(BaseModel):
    class MaterialItem(BaseModel):
        type: MaterialType
        name: str
        name_ko: str

    total: int
    items: list[MaterialItem] = []


class MaterialRequest(BaseModel):
    """
    GCS에 저장할 칵테일 레시피 JSON의 Material
    """
    type: MaterialType
    name: str
    name_ko: str
    unit: Unit
    amount: int
