from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.measurement import measurement_router
from api.spirit import spirit_schema, spirit_crud
from database import get_db

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

    _spirit_create.measurement = measurement_router.measurement_create(_measurement=_spirit_create.measurement, db=db)

    if spirit_crud.get_exist_spirit(db=db, _spirit=_spirit_create):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 Spirit입니다.")
    spirit_crud.create_spirit(db=db, _spirit=_spirit_create)
