from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.measurement import measurement_schema, measurement_crud
from database import get_db

router = APIRouter(
    prefix="/api/measurements",
)


@router.get("", response_model=measurement_schema.MeasurementList)
def measurement_list(db: Session = Depends(get_db)):
    total, _measurement_list = measurement_crud.get_measurement_list(db)
    return {'total': total, 'measurements': _measurement_list}


@router.get("/{measurement_id}", response_model=measurement_schema.Measurement)
def measurement_detail(measurement_id: int, db: Session = Depends(get_db)):
    measurement = measurement_crud.get_measurement(db, measurement_id=measurement_id)
    if not measurement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Measurement입니다.")
    else:
        return measurement


# is_post: bool = True -> measurement_create 함수가 post로 호출되었는지 확인
@router.post("", status_code=status.HTTP_201_CREATED)
def measurement_create(_measurement: measurement_schema.MeasurementCreate,
                       is_post: bool = True,
                       db: Session = Depends(get_db)):
    measurement = measurement_crud.get_exist_measurement(db=db, measurement=_measurement)
    if measurement and is_post:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 Measurement입니다.")
    elif measurement:
        return measurement
    else:
        measurement = measurement_crud.create_measurement(db=db, measurement_create=_measurement)
        return measurement


@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
def measurement_delete(measurement_id: int, db: Session = Depends(get_db)):
    if not measurement_crud.delete_measurement(db=db, measurement_id=measurement_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Measurement입니다.")
