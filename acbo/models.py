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


class Spirit(Base):
    __tablename__ = 'spirit'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(SpiritType), nullable=False)
    unit = Column(Enum(Unit), nullable=False)
    amount = Column(Integer, nullable=False)
    cocktail_id = Column(Integer, ForeignKey('cocktail.id'))
    # cocktail = relationship("Cocktail", backref="spirits")


class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(MaterialType), nullable=False)
    name = Column(String, nullable=False)
    name_ko = Column(String)
    unit = Column(Enum(Unit), nullable=False)
    amount = Column(Integer, nullable=False)
    cocktail_id = Column(Integer, ForeignKey('cocktail.id'), nullable=True)
    # cocktail = relationship("Cocktail", backref="materials")


class Cocktail(Base):
    __tablename__ = 'cocktail'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    name_ko = Column(String)
    skill = Column(Enum(Skill))
    usage_count = Column(Integer, default=0)

    spirits = relationship("Spirit", cascade="all, delete", backref="cocktail")
    materials = relationship("Material", cascade="all, delete", backref="cocktail")


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    # google_id = Column(Integer, nullable=True)
    username = Column(String(length=20), unique=True, nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)
    password = Column(String(length=255), nullable=False)
    created_at = Column(DateTime, default=datetime)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime)

    bookmarks = relationship("Bookmark", cascade="all, delete", backref="user")


class Bookmark(Base):
    __tablename__ = 'bookmark'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    cocktail_id = Column(Integer, ForeignKey('cocktail.id'))

    created_at = Column(DateTime, default=datetime)
    # cocktail = relationship("Cocktail", backref="bookmark")
