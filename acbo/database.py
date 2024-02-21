from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import SQLALCHEMY_DATABASE_URL

from sqlalchemy.orm import class_mapper


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False} # SQLite DB
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)


# 이벤트 리스너 함수 정의
def serdes_columns(target, action):
    for column in class_mapper(target.__class__).columns:
        if column.key in ['name', 'name_ko']:
            value = getattr(target, column.key)
            if value is not None:
                modified_value = value.replace(" ", "_") if action == 'serialize' else value.replace("_", " ")
                setattr(target, column.key, modified_value)
                # print(f"{action} {column.key}: {value} -> {modified_value}")


def after_select_listener(target, connection, **kwargs):
    serdes_columns(target, 'deserialize')


def before_insert_listener(mapper, connection, target):
    serdes_columns(target, 'serialize')


def before_update_listener(mapper, connection, target):
    serdes_columns(target, 'serialize')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
