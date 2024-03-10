from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from api.user import user_crud
from core.config import (
    ALGORITHM,
    MAIL_FROM,
    MAIL_FROM_NAME,
    MAIL_PASSWORD,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_USERNAME,
    SECRET_KEY,
)
from db.database import get_db

router = APIRouter(
    prefix="/api/oauth2/token",
    tags=["user"],
)

conf = ConnectionConfig(
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "template",
)
fm = FastMail(conf)


class Token(BaseModel):
    token: str


async def send_email_token(access_token: str, email: str):
    body = {
        "access_token": access_token,
    }
    try:
        message = MessageSchema(
            subject="[ACBO] Alcohol-Blackout 회원가입 인증 메일",
            recipients=[email],
            template_body=body,
            subtype=MessageType.html,
        )

        await fm.send_message(message, template_name="email.html")
        return body
    except Exception as e:
        return None


def _verify_email(db: Session, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="찾을 수 없는 토큰 값 입니다. ",
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="만료된 토큰입니다."
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="유효하지 않은 토큰입니다."
        )
    else:
        user = user_crud.get_user(db, email=email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="찾을 수 없는 유저입니다."
            )
        elif user.status == 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 인증된 이메일입니다.",
            )

        try:
            return user_crud.verified_email(db, user=user)
        except Exception as e:
            return None


@router.post("/", status_code=status.HTTP_200_OK)
def verify_email(token: Token, db: Session = Depends(get_db)):
    if not _verify_email(db, token.token):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="이메일 인증에 실패했습니다.",
        )
    return {"message": "이메일 인증이 완료되었습니다."}
