from pydantic import BaseModel, field_validator, Field

from models import MaterialType, Unit


class Material(BaseModel):
    id: int
    type: MaterialType
    name: str = Field(..., nullable=False, max_length=20)
    unit: Unit
    amount: int
    cocktail_id: int


class MaterialList(BaseModel):
    total: int
    materials: list[Material] = []


class MaterialCreate(BaseModel):
    type: MaterialType
    name: str = Field(..., nullable=False, max_length=20)
    unit: Unit
    amount: int
    cocktail_id: int

    @field_validator('type')
    def validate_material_type(cls, v):
        if v.name not in MaterialType.__members__:
            raise ValueError('존재하지 않는 재료 입니다.')
        return v

    @field_validator('unit')
    def unit_check(cls, v):
        # Web에서 Dropdown으로 Unit을 선택하면 상관 없음
        if v.name not in Unit.__members__:
            raise ValueError('존재하지 않는 단위 입니다.')
        return v

    @field_validator('amount')
    def amount_check(cls, v, values):
        print(v, values)
        if type(v) is not int:
            raise ValueError('숫자만 입력해주세요.')
        elif v <= 0 and values.data['unit'].name != 'Full_up':
            raise ValueError('0 이하의 숫자는 허용되지 않습니다.')
        return v


class MaterialUpdate(MaterialCreate):
    pass
