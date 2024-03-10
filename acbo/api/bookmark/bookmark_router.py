from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.bookmark import bookmark_crud, bookmark_schema
from api.user.user_router import get_current_active_user
from db.database import get_db
from models import User

router = APIRouter(
    prefix="/api/bookmarks",
    tags=["bookmark"],
)


@router.get("", response_model=bookmark_schema.BookmarkCocktailList)
def bookmark_cocktail_list(current_user: User = Depends(get_current_active_user)):
    """
    북마크에 등록된 칵테일 리스트를 반환합니다.
    ```json
        Args:
            None
        Returns: {
            "total": 5,
            "items": [
                {
                    "name": "Golden Dream",
                    "name_ko": "골든 드림",
                    "skill": "Shake",
                    "abv": 15
                },
                {
                    "name": "Dry Martini",
                    "name_ko": "드라이 마티니",
                    "skill": "Stir",
                    "abv": 30
                },
                {
                    "name": "Stinger",
                    "name_ko": "스팅어",
                    "skill": "Stir",
                    "abv": 26
                },
                {
                    "name": "Daiquiri",
                    "name_ko": "다이키리",
                    "skill": "Shake",
                    "abv": 22
                },
                {
                    "name": "Derby",
                    "name_ko": "더비",
                    "skill": "Stir",
                    "abv": 20
                }
            ]
        }
    ```
    """
    total, cocktails = bookmark_crud.get_bookmarked_cocktail_list(user=current_user)
    if not cocktails:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="북마크에 등록된 칵테일이 없습니다.",
        )
    return {"total": total, "items": cocktails}


@router.get("/{cocktail_id}", response_model=bookmark_schema.Bookmarked)
def bookmarked(cocktail_id: int, current_user: User = Depends(get_current_active_user)):
    return {
        "is_bookmarked": (
            True
            if bookmark_crud.get_is_bookmarked(
                user=current_user, cocktail_id=cocktail_id
            )
            else False
        )
    }


@router.post("/{cocktail_id}", status_code=status.HTTP_201_CREATED, response_model=None)
def bookmark_create(
    cocktail_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not bookmark_crud.create_bookmark(
        db, user=current_user, cocktail_id=cocktail_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="북마크 등록에 실패했습니다.",
        )
    return None


@router.delete("/{cocktail_id}", status_code=status.HTTP_204_NO_CONTENT)
def bookmark_delete(
    cocktail_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    bookmark_crud.delete_bookmark(db, user=current_user, cocktail_id=cocktail_id)
