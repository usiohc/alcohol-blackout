from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from api.material import material_crud, material_schema
from database import get_db
from models import SpiritType

router = APIRouter(
    prefix="/api/materials",
)


@router.get("", response_model=material_schema.MaterialList)
def material_list(db: Session = Depends(get_db)):
    total, _material_list = material_crud.get_material_list(db=db)
    return {'total': total, 'materials': _material_list}


@router.get("/{material_id}", response_model=material_schema.Material)
def material_detail(material_id: int, db: Session = Depends(get_db)):
    material = material_crud.get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Material입니다.")
    return material




@router.post("", status_code=status.HTTP_201_CREATED)
def material_create(_material_create: material_schema.MaterialCreate,
                    db: Session = Depends(get_db)):
    if material_crud.get_exist_material(db=db, material=_material_create):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 Material입니다.")
    material_crud.create_material(db=db, material=_material_create)


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def material_delete(material_id: int, db: Session = Depends(get_db)):
    if not material_crud.get_material(db=db, material_id=material_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Material입니다.")
    material_crud.delete_material(db=db, material_id=material_id)


@router.put("/{material_id}", status_code=status.HTTP_200_OK)
def material_update(material_id: int,
                    _material_update: material_schema.MaterialUpdate,
                    db: Session = Depends(get_db)):
    material = material_crud.get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Material입니다.")

    # 입력받은 Material이 이미 존재하는지 확인
    if material_crud.get_exist_material(db=db, material=_material_update):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 Material입니다.")

    material_crud.update_material(db=db, db_material=material, material_update=_material_update)
    return _material_update


# 재료 탭
@router.get("/", response_model=material_schema.MaterialBySpirit)
def material_by_spirits(spirit_type: str = Query("", convert_underscores=False),
                        db: Session = Depends(get_db)):
    _spirit_type = []
    if spirit_type:
        _spirit_type = spirit_type.split(",")
    if not all(spirit_type in SpiritType.__members__ for spirit_type in _spirit_type):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="올바르지 않은 Spirit Type 입니다.")

    total, materials = material_crud.get_material_by_spirits(spirit_type=_spirit_type, db=db)

    if not materials:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material을 찾을 수 없습니다.")
    return {"total": total, "items": materials}
