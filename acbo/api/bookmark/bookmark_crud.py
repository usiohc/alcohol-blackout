from datetime import datetime

from sqlalchemy.orm import Session
from models import Bookmark, User


def create_bookmark(db: Session, user: User, cocktail_id: int):
    db_bookmark = Bookmark(user_id=user.id, cocktail_id=cocktail_id)
    db.add(db_bookmark)
    db.commit()


def delete_bookmark(db: Session, user: User, cocktail_id: int):
    db_bookmark = db.query(Bookmark).filter(Bookmark.user_id == user.id,
                                           Bookmark.cocktail_id == cocktail_id).first()
    db.delete(db_bookmark)
    db.commit()


def get_bookmark_list(user: User):
    return user.bookmarks
