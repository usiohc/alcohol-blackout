from pydantic import BaseModel, field_validator

from models import Unit


class Measurement(BaseModel):
    id: int
    unit: Unit
    amount: int
    usage_count: int = 0


class MeasurementCreate(BaseModel):
    unit: Unit
    amount: int

    @field_validator('unit')
    def unit_check(cls, v):
        # Web에서 Dropdown으로 Unit을 선택하면 상관 없음
        if v.name not in Unit.__members__:
            raise ValueError('존재하지 않는 단위 입니다.')
        return v

    @field_validator('amount')
    def amount_check(cls, v):
        if type(v) is not int:
            raise ValueError('숫자만 입력해주세요.')
        elif v <= 0:
            raise ValueError('0 이하의 숫자는 허용되지 않습니다.')
        return v
