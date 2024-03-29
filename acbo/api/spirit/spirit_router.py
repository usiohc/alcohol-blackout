from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.cocktail import cocktail_crud
from api.spirit import spirit_crud, spirit_schema
from api.user.user_router import get_current_superuser
from db.database import get_db
from models import User

router = APIRouter(
    prefix="/api/spirits",
    tags=["spirit"],
)


@router.get("", response_model=spirit_schema.SpiritList)
def spirit_list(db: Session = Depends(get_db)):
    total, _spirit_list = spirit_crud.get_spirit_list(db)
    return {"total": total, "spirits": _spirit_list}


@router.get("/{spirit_id}", response_model=spirit_schema.Spirit)
def spirit_detail(spirit_id: int, db: Session = Depends(get_db)):
    spirit = spirit_crud.get_spirit(db, spirit_id=spirit_id)
    if not spirit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Spirit입니다."
        )
    return spirit


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=spirit_schema.Spirit
)
def spirit_create(
    _spirit_create: spirit_schema.SpiritCreate,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_superuser),
):
    """
    ```json
    Args:
        _spirit_create: {
            "type": "Vodka", (Enum)
            "name": "str" || "", (Nullable)
            "name_ko": "str" || "", (Nullable)
            "unit": "ml", (Enum)
            "amount": 0, (1 이상)
            "cocktail_id": Optional[int]
        }
    Returns:
        {
            "id": 1,
            "type": "Vodka",
            "name": "str",
            "name_ko": "str",
            "unit": "ml",
            "amount": 1,
            "cocktail_id": null
        }
    ```
    """
    if not _spirit_create.cocktail_id:
        _spirit_create.cocktail_id = None
    elif (
        cocktail_crud.get_cocktail(db=db, cocktail_id=_spirit_create.cocktail_id)
        is None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="cocktail_id에 해당하는 칵테일를 찾을 수 없습니다.",
        )

    created_spirit = spirit_crud.create_spirit(db=db, spirit=_spirit_create)
    return created_spirit


@router.put(
    "/{spirit_id}", status_code=status.HTTP_200_OK, response_model=spirit_schema.Spirit
)
def spirit_update(
    spirit_id: int,
    _spirit_update: spirit_schema.SpiritUpdate,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_superuser),
):
    spirit = spirit_crud.get_spirit(db=db, spirit_id=spirit_id)
    if not spirit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 Spirit입니다.",
        )

    if not _spirit_update.cocktail_id:
        _spirit_update.cocktail_id = None
    elif (
        cocktail_crud.get_cocktail(db=db, cocktail_id=_spirit_update.cocktail_id)
        is None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="cocktail_id에 해당하는 칵테일를 찾을 수 없습니다.",
        )

    updated_spirit = spirit_crud.update_spirit(
        db=db, db_spirit=spirit, spirit_update=_spirit_update
    )
    return updated_spirit


@router.delete("/{spirit_id}", status_code=status.HTTP_204_NO_CONTENT)
def spirit_delete(
    spirit_id: int,
    db: Session = Depends(get_db),
    superuser: User = Depends(get_current_superuser),
):
    if not spirit_crud.get_spirit(db=db, spirit_id=spirit_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 Spirit입니다."
        )
    spirit_crud.delete_spirit(db=db, spirit_id=spirit_id)
