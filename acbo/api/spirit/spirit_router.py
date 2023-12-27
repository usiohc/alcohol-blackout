from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from api.spirit import spirit_schema, spirit_crud
from api.measurement import measurement_schema, measurement_crud

router = APIRouter(
    prefix="/api/spirit",
)


@router.get("/list", response_model=list[spirit_schema.Spirit])
def spirit_list(db: Session = Depends(get_db)):
    _spirit_list = spirit_crud.get_spirit_list(db)
    return _spirit_list


@router.get("/detail/{spirit_id}")
def spirit_detail(spirit_id: int, db: Session = Depends(get_db)):
    spirit = spirit_crud.get_spirit(db, spirit_id=spirit_id)
    return spirit


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def spirit_create(_spirit_create: spirit_schema.SpiritCreate,
                  db: Session = Depends(get_db)):
    # measurement:

    if measurement := measurement_crud.get_exist_measurement(db=db, measurement=_spirit_create.measurement) is None:
        _spirit_create.measurement = measurement_crud.create_measurement(db=db, measurement_create=_spirit_create.measurement)
    spirit_crud.create_spirit(db=db, spirit=_spirit_create, measurement_id=_spirit_create.measurement.id)
