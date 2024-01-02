from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.cocktail import cocktail_crud, cocktail_schema
from database import get_db

router = APIRouter(
    prefix="/api/cocktails",
)


@router.get("", response_model=cocktail_schema.CocktailList)
def cocktail_list(db: Session = Depends(get_db)):
    total, _cocktail_list = cocktail_crud.get_cocktail_list(db)
    return {'total': total, 'cocktails': _cocktail_list}


@router.get("/{cocktail_id}", response_model=cocktail_schema.Cocktail)
def cocktail_detail(cocktail_id: int, db: Session = Depends(get_db)):
    cocktail = cocktail_crud.get_cocktail(db, cocktail_id=cocktail_id)
    if not cocktail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")
    return cocktail


@router.get("/{cocktail_id}/spirits", response_model=cocktail_schema.CocktailSpiritList)
def cocktail_spirit_list(cocktail_id: int, db: Session = Depends(get_db)):
    total, _cocktail_spirit_list = cocktail_crud.get_cocktail_spirit_list(db, cocktail_id=cocktail_id)
    if not _cocktail_spirit_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")
    return {'total': total, 'spirits': _cocktail_spirit_list}


@router.get("/{cocktail_id}/materials", response_model=cocktail_schema.CocktailMaterialList)
def cocktail_material_list(cocktail_id: int, db: Session = Depends(get_db)):
    total, _cocktail_material_list = cocktail_crud.get_cocktail_material_list(db, cocktail_id=cocktail_id)
    if not _cocktail_material_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")
    return {'total': total, 'materials': _cocktail_material_list}


@router.post("", status_code=status.HTTP_201_CREATED)
def cocktail_create(_cocktail_create: cocktail_schema.CocktailCreate,
                    db: Session = Depends(get_db)):
    if cocktail_crud.get_exist_cocktail(db=db, cocktail=_cocktail_create):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 Cocktail입니다.")
    cocktail_crud.create_cocktail(db=db, cocktail=_cocktail_create)


@router.delete("/{cocktail_id}", status_code=status.HTTP_204_NO_CONTENT)
def cocktail_delete(cocktail_id: int, db: Session = Depends(get_db)):
    if not cocktail_crud.get_cocktail(db=db, cocktail_id=cocktail_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")
    cocktail_crud.delete_cocktail(db=db, cocktail_id=cocktail_id)


@router.put("/{cocktail_id}", status_code=status.HTTP_200_OK)
def cocktail_update(cocktail_id: int,
                    _cocktail_update: cocktail_schema.CocktailUpdate,
                    db: Session = Depends(get_db)):
    cocktail = cocktail_crud.get_cocktail(db=db, cocktail_id=cocktail_id)
    if not cocktail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Cocktail입니다.")

    # 입력받은 Cocktail이 이미 존재하는지 확인
    if cocktail_crud.get_exist_cocktail(db=db, cocktail=_cocktail_update):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 Cocktail입니다.")

    cocktail_crud.update_cocktail(db=db, db_cocktail=cocktail, cocktail_update=_cocktail_update)
    return _cocktail_update
