from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status

from api.user.user_crud import pwd_context
from database import get_db
from api.user import user_crud, user_schema
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from models import datetime

router = APIRouter(
    prefix="/api/users",
)


@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    if user_crud.get_existing_username(db=db, username=_user_create.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 닉네임입니다.")
    if user_crud.get_existing_email(db=db, email=_user_create.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 이메일입니다.")

    user_crud.create_user(db=db, user_create=_user_create)


@router.post("/login", response_model=user_schema.Token)
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

    # make access token
    data = {
        "sub": email,
        "exp": datetime + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": email
    }


    # return user
