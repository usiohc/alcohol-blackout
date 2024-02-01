from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import FieldValidationInfo

from models import SpiritType, Unit


class Spirit(BaseModel):
    id: int
    type: SpiritType
    name: str
    name_ko: str
    unit: Unit
    amount: int
    cocktail_id: int


class SpiritList(BaseModel):
    total: int
    spirits: list[Spirit] = []


class SpiritCreate(BaseModel):
    type: SpiritType
    name: str
    name_ko: str
    unit: Unit
    amount: int
    cocktail_id: int

    @field_validator('type', 'unit', 'amount')
    def validate_material(cls, v):
        if not v or not v.strip():
            raise PydanticCustomError("ValueError",
                                      "빈 값은 허용되지 않습니다.",
                                      {"value": v})
        return v


    @field_validator('type')
    def validate_spirit_type(cls, v):
        if v.name not in SpiritType.__members__:
            raise ValueError('존재하지 않는 기주 입니다.')
        return v

    @field_validator('unit')
    def unit_check(cls, v):
        # Web에서 Dropdown으로 Unit을 선택하면 상관 없음
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


class SpiritUpdate(SpiritCreate):
    pass


class SpiritRequest(BaseModel):
    """
    GCS에 저장할 칵테일 레시피 JSON의 Spirit
    """
    type: SpiritType
    name: str
    name_ko: str
    unit: Unit
    amount: int
