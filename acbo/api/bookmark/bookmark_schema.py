from pydantic import BaseModel

from api.cocktail.cocktail_schema import Cocktail


class Bookmark(BaseModel):
    user_id: int
    cocktail_id: int
    created_at: str


class BookmarkList(BaseModel):
    total: int
    bookmarks: list[Bookmark]


class BookmarkCocktailList(BaseModel):
    total: int
    cocktails: list[Cocktail] = []
