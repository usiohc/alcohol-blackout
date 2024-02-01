from enum import Enum as myEnum
from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base

KST = timezone(timedelta(hours=9))
datetime = datetime.now(KST)


class Skill(myEnum):
    Build = 'Build'
    Stir = 'Stir'
    Shake = 'Shake'
    Float = 'Float'
    Blend = 'Blend'


class Unit(myEnum):
    """
    ml: 밀리리터
    tsp: 티스푼
    dash: 5방울, 1ml
    drop: 방울, 0.2ml
    pinch: 꼬집
    Full_up: 취향껏
    piece: 조각
    """

    ml = 'ml'
    tsp = 'tsp'
    dash = 'dash'
    drop = 'drop'
    pinch = 'pinch'
    Full_up = 'Full_up' # Full_up -> amount = 0
    piece = 'piece'


class SpiritType(myEnum):
    Vodka = 'Vodka'
    Gin = 'Gin'
    Rum = 'Rum'
    Tequila = 'Tequila'
    Whisky = 'Whisky'
    Brandy = 'Brandy'
    Liqueur = 'Liqueur'
    Beer = 'Beer'
    Wine = 'Wine'


class MaterialType(myEnum):
    Liqueur = 'Liqueur'
    Syrup = 'Syrup'
    Juice = 'Juice'
    Soda = 'Soda'
    Garnish = 'Garnish'
    Etc = 'Etc'


class Spirit(Base):
    __tablename__ = 'spirit'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(SpiritType), nullable=False)
    name = Column(String(length=50), nullable=True) # '' 일 경우 anything, 무엇이든 상관 없음.
    name_ko = Column(String(length=50), nullable=True)
    unit = Column(Enum(Unit), nullable=False)
    amount = Column(Integer, nullable=False)
    cocktail_id = Column(Integer, ForeignKey('cocktail.id'))
    # cocktail = relationship("Cocktail", backref="spirits")


class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(MaterialType), nullable=False)
    name = Column(String(length=50), nullable=False)
    name_ko = Column(String(length=50), nullable=False)
    unit = Column(Enum(Unit), nullable=False)
    amount = Column(Integer, nullable=False)
    cocktail_id = Column(Integer, ForeignKey('cocktail.id'), nullable=True)
    # cocktail = relationship("Cocktail", backref="materials")


class Cocktail(Base):
    __tablename__ = 'cocktail'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    name_ko = Column(String(length=50), nullable=False)
    abv = Column(Integer, nullable=False)
    skill = Column(Enum(Skill), nullable=False)
    usage_count = Column(Integer, default=0)

    spirits = relationship("Spirit", cascade="all, delete", backref="cocktail")
    materials = relationship("Material", cascade="all, delete", backref="cocktail")


class User(Base):
    """
    id: int
    username: 닉네임
    email: 이메일, 로그인에 사용됨
    password: 비밀번호
    created_at: 생성일
    updated_at: 수정일
    status: {
        0: 일반 유저 -> 이메일 인증 X, 로그인 불가
        1: 일반 유저 -> 이메일 인증 O, 로그인 가능
        2: 관리자
    }
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    # google_id = Column(Integer, nullable=True)
    username = Column(String(length=20), unique=True, nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    created_at = Column(DateTime, default=datetime)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime)
    status = Column(Integer, default=0)

    bookmarks = relationship("Bookmark", cascade="all, delete", backref="user")


class Bookmark(Base):
    __tablename__ = 'bookmark'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    cocktail_id = Column(Integer, ForeignKey('cocktail.id'))

    created_at = Column(DateTime, default=datetime)
    cocktails = relationship("Cocktail", backref="bookmark")
