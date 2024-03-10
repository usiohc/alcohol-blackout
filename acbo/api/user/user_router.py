from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from api.user import user_crud, user_schema
from api.user.email.email import send_email_token
from api.user.user_crud import pwd_context
from api.user.user_schema import oauth2_scheme
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, datetime
from db.database import get_db
from models import User

router = APIRouter(
    prefix="/api/users",
    tags=["user"],
)


def make_access_token(email: str, exp: int):
    data = {"email": email, "exp": datetime() + timedelta(minutes=exp)}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, email=email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="찾을 수 없는 사용자입니다.",
            )
        return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증되지 않은 사용자입니다.",
        )
    return current_user


def get_current_superuser(current_user: User = Depends(get_current_user)):
    if current_user.status != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 없습니다."
        )
    return current_user


@router.post("/register", status_code=status.HTTP_200_OK)
async def user_register(
    _user_create: user_schema.UserCreate, db: Session = Depends(get_db)
):
    if user_crud.get_existing_username(db=db, username=_user_create.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 닉네임입니다."
        )
    if user_crud.get_user(db=db, email=_user_create.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 이메일입니다."
        )

    user = user_crud.create_user(db=db, user_create=_user_create)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="유저 생성에 실패했습니다.",
        )

    access_token = make_access_token(user.email, 30)
    if not await send_email_token(access_token, user.email):
        user_crud.delete_user(db, user)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="인증 메일 전송에 실패했습니다.",
        )

    return {"message": "회원가입이 완료되었습니다. 이메일을 확인해주세요."}


@router.post("/login", response_model=user_schema.UserLogin)
def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    email = form_data.username
    password = form_data.password

    # 유저 email 확인
    user = user_crud.get_user(db=db, email=email)
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 혹은 비밀번호가 일치하지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 인증이 완료되지 않았습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = make_access_token(email, ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": email,
        "username": user.username,
    }


@router.get("/me", response_model=user_schema.UserBase)
def user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.patch("/username", status_code=status.HTTP_200_OK)
def user_update_username(
    _user_update_username: user_schema.UserUpdateUsername,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    username = _user_update_username.username
    if user_crud.get_existing_username(db, username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 닉네임입니다."
        )
    if not user_crud.update_username(db, user=current_user, username=username):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="닉네임 수정에 실패했습니다.",
        )
    return {"message": "닉네임이 수정되었습니다."}


@router.patch("/password", status_code=status.HTTP_200_OK)
def user_update_password(
    _user_update_password: user_schema.UserUpdatePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    password = _user_update_password.password
    if pwd_context.verify(password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="기존 비밀번호와 동일합니다.",
        )

    if not user_crud.update_password(db, user=current_user, password=password):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="비밀번호 수정에 실패했습니다.",
        )
    return {"message": "비밀번호가 수정되었습니다."}


@router.delete("", status_code=status.HTTP_200_OK)
def user_delete(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    user_crud.delete_user(db, user=current_user)
    return {"message": "회원탈퇴가 완료되었습니다."}
