from typing import List, Optional

from pydantic import BaseModel, field_validator

from models import SpiritType, Unit


class SpiritBase(BaseModel):
    type: SpiritType
    name: str
    name_ko: str
    unit: Unit
    amount: int


class Spirit(SpiritBase):
    id: int
    cocktail_id: Optional[int]


class SpiritList(BaseModel):
    total: int
    spirits: List[Spirit] = []


class SpiritBaseCreate(SpiritBase):
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


class SpiritCreate(SpiritBaseCreate):
    cocktail_id: Optional[int]


class SpiritUpdate(SpiritCreate):
    pass


class SpiritRequest(SpiritBaseCreate):
    """
    GCS에 저장할 칵테일 레시피 JSON의 Spirit
    """
    pass
