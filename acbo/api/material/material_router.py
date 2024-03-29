from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from api.cocktail import cocktail_crud
from api.material import material_crud, material_schema
from api.user.user_router import get_current_superuser
from core.enums import SpiritType
from db.database import get_db
from models import User

router = APIRouter(
    prefix="/api/materials",
    tags=["material"],
)


@router.get("", response_model=material_schema.MaterialList)
def material_list(db: Session = Depends(get_db)):
    total, _material_list = material_crud.get_material_list(db=db)
    return {"total": total, "materials": _material_list}


@router.get("/{material_id:int}", response_model=material_schema.Material)
def material_detail(material_id: int, db: Session = Depends(get_db)):
    material = material_crud.get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 Material입니다.",
        )
    return material


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=material_schema.Material
)
def material_create(
    _material_create: material_schema.MaterialCreate,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_superuser),
):
    """
    ```json
    Args:
        _material_create: {
            "type": "Spirit", (Enum)
            "name": "str", (NotNull)
            "name_ko": "str", (NotNull)
            "unit": "ml", (Enum)
            "amount": 0, (1 이상)
            "cocktail_id": Optional[int]
        }
    Returns:
        {
            "id": 1,
            "type": "Spirit",
            "name": "str",
            "name_ko": "str",
            "unit": "ml",
            "amount": 1,
            "cocktail_id": null
        }
    ```
    """
    if not _material_create.cocktail_id:
        _material_create.cocktail_id = None
    elif (
        cocktail_crud.get_cocktail(db=db, cocktail_id=_material_create.cocktail_id)
        is None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 Cocktail입니다.",
        )

    created_material = material_crud.create_material(db=db, material=_material_create)
    return created_material


@router.put(
    "/{material_id}",
    status_code=status.HTTP_200_OK,
    response_model=material_schema.Material,
)
def material_update(
    material_id: int,
    _material_update: material_schema.MaterialUpdate,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_superuser),
):
    material = material_crud.get_material(db=db, material_id=material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 Material입니다.",
        )

    if not _material_update.cocktail_id:
        _material_update.cocktail_id = None
    elif (
        cocktail_crud.get_cocktail(db=db, cocktail_id=_material_update.cocktail_id)
        is None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="cocktail_id에 해당하는 칵테일를 찾을 수 없습니다.",
        )

    updated_material = material_crud.update_material(
        db=db, db_material=material, material_update=_material_update
    )
    return updated_material


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def material_delete(
    material_id: int,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_superuser),
):
    if not material_crud.get_material(db=db, material_id=material_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 Material입니다.",
        )
    material_crud.delete_material(db=db, material_id=material_id)


@router.get("/", response_model=material_schema.MaterialListBySpirit)
def material_by_spirit(
    spirits: str = Query("", convert_underscores=False), db: Session = Depends(get_db)
):
    """
    ```json
    Args:
        spirits: (Query parameter, sep=",") default: "" -> 모든 Material 을 반환
             "Vodka,Whiskey"
    Returns:
        {
            "total": 20,
            "items": [
                {
                    "type": "Liqueur",
                    "name": "Absinthe",
                    "name_ko": "압생트",
                },
                {
                    "type": "Liqueur"
                    "name": "Angostura Bitters",
                    "name_ko": "앙고스투라 비터스",
                },
                ...
            }
    ```
    """
    # "Vodka,Whiskey" -> ["Vodka", "Whiskey"] || "" -> []
    _spirits = [s.capitalize() for s in spirits.split(",")] if spirits else []
    if _spirits and not all(s in SpiritType.__members__ for s in _spirits):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="올바르지 않은 Spirit Type 입니다.",
        )

    total, materials = material_crud.get_material_by_spirit(spirits=_spirits, db=db)
    if not materials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Material을 찾을 수 없습니다."
        )
    return {"total": total, "items": materials}
