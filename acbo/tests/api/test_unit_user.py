from api.user import user_schema, user_crud
from api.user.user_crud import pwd_context
from api.user.user_router import make_access_token


def test_create_user(db):
    user_data = {
        "username": "test_user",
        "email": "test_user@test.com",
        "password": "test_password",
        "passwordCheck": "test_password"
    }
    created_user = user_crud.create_user(db, user_schema.UserCreate(**user_data))
    assert created_user.username == user_data["username"]
    assert created_user.email == user_data["email"]
    assert pwd_context.verify(user_data["password"], created_user.password) is True


def test_get_existing_username(db, user):
    existing_user = user_crud.get_existing_username(db, user.username)
    assert existing_user.username == user.username

    not_existing_user = user_crud.get_existing_username(db, "not_existing_user")
    assert not_existing_user is None


def test_get_user(db, user):
    get_user = user_crud.get_user(db, user.email)
    assert get_user.username == user.username
    assert get_user.email == user.email
    assert get_user.password == user.password


def test_verified_email(db, user):
    verified_user = user_crud.verified_email(db, user)
    assert verified_user.status == user.status == 1


def test_update_username(db, user):
    new_username = "new_test_user"
    updated_user = user_crud.update_username(db, user, new_username)
    assert updated_user.username == new_username


def test_update_password(db, user):
    new_password = "new_test_password"
    updated_user = user_crud.update_password(db, user, new_password)
    assert pwd_context.verify(new_password, updated_user.password) is True


def test_delete_user(db, user):
    user_crud.delete_user(db, user)
    deleted_user = user_crud.get_user(db, user.email)
    assert deleted_user is None


def test_send_email_token_and_verify_email(db, user):
    import asyncio
    from api.user.email.email import send_email_token, _verify_email, fm

    access_token = make_access_token(user.email, 1)
    fm.config.SUPPRESS_SEND = 1 # 실제 전송 X
    send_email = asyncio.run(send_email_token(access_token, user.email))
    assert send_email is not None

    verified_user = _verify_email(db, access_token)
    assert verified_user.status == 1
