from pydantic import BaseModel, field_validator

from models import SpiritType, Unit

from api.measurement.measurement_schema import MeasurementCreate


class Spirit(BaseModel):
    id: int
    type: SpiritType
    measurement_id: int
    usage_count: int


class SpiritCreate(BaseModel):
    type: SpiritType
    # measurement_id: int
    measurement: MeasurementCreate

    @field_validator('type')
    def validate_spirit_type(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        elif v not in SpiritType.__members__:
            raise ValueError('존재하지 않는 술입니다.')
        return v
