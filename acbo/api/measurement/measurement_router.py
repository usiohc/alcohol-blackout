from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.measurement import measurement_schema, measurement_crud
from database import get_db

router = APIRouter(
    prefix="/api/measurement",
)


@router.get("/list", response_model=list[measurement_schema.Measurement])
def measurement_list(db: Session = Depends(get_db)):
    _measurement_list = measurement_crud.get_measurement_list(db)
    return _measurement_list


@router.get("/detail/{measurement_id}", response_model=measurement_schema.Measurement)
def measurement_detail(measurement_id: int, db: Session = Depends(get_db)):
    measurement = measurement_crud.get_measurement(db, measurement_id=measurement_id)
    return measurement


# @router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
# def measurement_create(_measurement_create: spirit_schema.SpiritCreate.measurement,
def measurement_create(_measurement: measurement_schema.MeasurementCreate,
                       db: Session = Depends(get_db)):

    measurement = measurement_crud.get_exist_measurement(db=db, _measurement=_measurement)
    if not measurement:
        measurement = measurement_crud.create_measurement(db=db, _measurement_create=_measurement)
    return measurement
