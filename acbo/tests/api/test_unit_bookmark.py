from api.bookmark import bookmark_crud


def test_get_bookmarked_cocktail_list(db, verified_user, cocktail, bookmark):
    total, cocktail_list = bookmark_crud.get_bookmarked_cocktail_list(verified_user)
    assert total == 1
    assert cocktail_list[0].id == cocktail.id
    assert cocktail_list[0].name == cocktail.name.replace("_", " ")
    assert cocktail_list[0].name_ko == cocktail.name_ko.replace("_", " ")
    assert cocktail_list[0].skill == cocktail.skill
    assert cocktail_list[0].abv == cocktail.abv


def test_get_is_bookmarked(db, verified_user, cocktail, bookmark):
    is_bookmarked = bookmark_crud.get_is_bookmarked(verified_user, cocktail.id)
    assert is_bookmarked is True

    is_not_bookmarked = bookmark_crud.get_is_bookmarked(verified_user, cocktail.id + 1)
    assert is_not_bookmarked is False


def test_create_bookmark(db, verified_user, cocktail):
    bookmark = bookmark_crud.create_bookmark(db, verified_user, cocktail.id)
    assert bookmark.user_id == verified_user.id
    assert bookmark.cocktail_id == cocktail.id
    assert bookmark.id is not None


def test_delete_bookmark(db, verified_user, cocktail, bookmark):
    bookmark_crud.delete_bookmark(db, verified_user, cocktail.id)
    is_bookmarked = bookmark_crud.get_is_bookmarked(verified_user, cocktail.id)
    assert is_bookmarked is False
