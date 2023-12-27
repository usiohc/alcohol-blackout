from pydantic import BaseModel, field_validator

from models import Unit


class Measurement(BaseModel):
    id: int
    unit: Unit
    amount: int


class MeasurementCreate(BaseModel):
    unit: Unit
    amount: int

    @field_validator('unit', 'amount')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('unit')
    def unit_check(cls, v):
        # Web에서 Dropdown으로 Unit을 선택하면 상관 없음
        if v not in Unit.__members__:
            raise ValueError('존재하지 않는 술입니다.')
        return v

    @field_validator('amount')
    def amount_check(cls, v):
        if v is not int:
            raise ValueError('숫자만 입력해주세요.')
        elif v <= 0:
            raise ValueError('0 이하의 숫자는 허용되지 않습니다.')
        return v
