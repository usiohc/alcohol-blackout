from passlib.context import CryptContext
from sqlalchemy.orm import Session
from api.user import user_schema
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: user_schema.UserCreate):
    db_user = User(username=user_create.username,
                   email=user_create.email,
                   password=pwd_context.hash(user_create.password))
    db.add(db_user)
    db.commit()


def get_existing_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_existing_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
