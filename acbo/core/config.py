import os
from datetime import datetime as dt
from datetime import timedelta, timezone

DEBUG = os.getenv("DEBUG")
LOCAL_ORIGINS = os.getenv("LOCAL_ORIGINS").split(",")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
SQLALCHEMY_DATABASE_URL = (
    f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")

SWAGGER_USER = os.getenv("SWAGGER_USER")
SWAGGER_PASSWORD = os.getenv("SWAGGER_PASSWORD")


KST = timezone(timedelta(hours=9))


def datetime():
    return dt.now(KST)


def datetime_date():
    return dt.now(KST).date()
