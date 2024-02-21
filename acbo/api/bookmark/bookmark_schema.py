from typing import List

from pydantic import BaseModel

from api.cocktail.cocktail_schema import CocktailBase


class Bookmark(BaseModel):
    user_id: int
    cocktail_id: int
    created_at: str


class BookmarkList(BaseModel):
    total: int
    bookmarks: List[Bookmark]


class BookmarkCocktailList(BaseModel):
    total: int
    items: List[CocktailBase] = []


class Bookmarked(BaseModel):
    is_bookmarked: bool
