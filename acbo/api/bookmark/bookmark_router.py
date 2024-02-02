from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from api.bookmark import bookmark_schema, bookmark_crud
from api.cocktail import cocktail_crud
from api.user.user_router import get_current_user
from database import get_db
from models import User

router = APIRouter(
    prefix="/api/bookmarks",
    tags=["bookmark"],
)


@router.post("/{cocktail_id}", status_code=status.HTTP_201_CREATED)
def bookmark_create(cocktail_id: int,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    bookmark_crud.create_bookmark(db, user=current_user, cocktail_id=cocktail_id)


@router.delete("/{cocktail_id}", status_code=status.HTTP_204_NO_CONTENT)
def bookmark_delete(cocktail_id: int,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    bookmark_crud.delete_bookmark(db, user=current_user, cocktail_id=cocktail_id)


@router.get("", response_model=bookmark_schema.BookmarkCocktailList)
def bookmark_cocktail_list(db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    _bookmark_list = bookmark_crud.get_bookmark_list(user=current_user)
    if not _bookmark_list:
        return {'total': 0, 'cocktails': []}
    cocktail_id_list = [bookmark.cocktail_id for bookmark in _bookmark_list]
    total, cocktails = cocktail_crud.get_cocktail_bookmark_list(db, cocktail_id_list=cocktail_id_list)
    return {'total': total, 'items': cocktails}


@router.get("/{cocktail_id}", response_model=bookmark_schema.Bookmarked)
def bookmarked(cocktail_id: int,
                db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    if bookmark_crud.get_is_bookmarked(db, user=current_user, cocktail_id=cocktail_id):
        return {'is_bookmarked': True}
    return {'is_bookmarked': False}
