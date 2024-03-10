from sqlalchemy.orm import Session

from models import Bookmark, User


def get_bookmarked_cocktail_list(user: User):
    bookmark_list = user.bookmarks
    cocktail_list = [bookmark.cocktails for bookmark in bookmark_list]
    return len(cocktail_list), cocktail_list


def get_is_bookmarked(user: User, cocktail_id: int):
    bookmark_list = user.bookmarks
    if cocktail_id in [bookmark.cocktail_id for bookmark in bookmark_list]:
        return True
    return False


def create_bookmark(db: Session, user: User, cocktail_id: int):
    db_bookmark = Bookmark(user_id=user.id, cocktail_id=cocktail_id)
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark


def delete_bookmark(db: Session, user: User, cocktail_id: int):
    db_bookmark = (
        db.query(Bookmark)
        .filter(Bookmark.user_id == user.id, Bookmark.cocktail_id == cocktail_id)
        .first()
    )
    db.delete(db_bookmark)
    db.commit()
