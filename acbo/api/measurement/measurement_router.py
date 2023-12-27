from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import Measurement
from api.measurement import measurement_schema, measurement_crud

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


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def measurement_create(_measurement_create: measurement_schema.MeasurementCreate,
                       db: Session = Depends(get_db)):
    if measurement := measurement_crud.get_exist_measurement(db=db, measurement_create=_measurement_create):
        return measurement
    else:
        return measurement_crud.create_measurement(db=db, measurement_create=_measurement_create)
