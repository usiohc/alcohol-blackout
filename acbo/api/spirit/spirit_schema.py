from pydantic import BaseModel, field_validator

from api.measurement.measurement_schema import MeasurementCreate
from models import SpiritType


class Spirit(BaseModel):
    id: int
    type: SpiritType
    measurement_id: int
    usage_count: int = 0


class SpiritCreate(BaseModel):
    type: SpiritType
    # measurement_id: int
    measurement: MeasurementCreate

    @field_validator('type')
    def validate_spirit_type(cls, v):
        if v.name not in SpiritType.__members__:
            raise ValueError('존재하지 않는 주류 입니다.')
        return v
