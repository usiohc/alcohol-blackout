from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api.user import user_schema
from models import User, datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: user_schema.UserCreate):
    try:
        db_user = User(username=user_create.username,
                       email=user_create.email,
                       password=pwd_context.hash(user_create.password))
        db.add(db_user)
        db.commit()
        return True
    except Exception as e:
        print("create_user 실패")
        print(e)
        return False


def get_existing_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def verified_email(db: Session, user: User):
    user.status = 1
    db.add(user)
    db.commit()


def update_username(db: Session, user: User, username: str):
    user.username = username
    user.updated_at = datetime()
    db.add(user)
    db.commit()
    db.refresh(user)


def update_password(db, user: User, password: str):
    user.password = pwd_context.hash(password)
    user.updated_at = datetime()
    db.add(user)
    db.commit()
    db.refresh(user)


def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
