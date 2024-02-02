from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from api.user.email.email import send_email_token
from api.user.user_crud import pwd_context
from api.user.user_schema import oauth2_scheme
from database import get_db
from api.user import user_crud, user_schema
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models import datetime

router = APIRouter(
    prefix="/api/users",
    tags=["user"],
)


@router.post("/register", status_code=status.HTTP_200_OK)
async def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    if user_crud.get_existing_username(db=db, username=_user_create.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 닉네임입니다.")
    if user_crud.get_existing_email(db=db, email=_user_create.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 이메일입니다.")

    user = user_crud.create_user(db=db, user_create=_user_create)
    if not user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="유저 생성에 실패했습니다.")

    data = {
        "email": _user_create.email,
        "exp": datetime + timedelta(minutes=30)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    await send_email_token(access_token, _user_create.email)
    return {"message": "회원가입이 완료되었습니다. 이메일을 확인해주세요."}


@router.post("/login", response_model=user_schema.UserLogin)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    email = form_data.username
    password = form_data.password

    # 유저 email 확인
    user = user_crud.get_user(db=db, email=email)
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="이메일 혹은 비밀번호가 일치하지 않습니다.",
                            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.status == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="이메일 인증이 완료되지 않았습니다.",
                            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": email,
        "exp": datetime + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": email,
        "username": user.username,
    }


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, email=email)
        if user is None:
            raise credentials_exception
        return user
