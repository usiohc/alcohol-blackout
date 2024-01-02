from enum import Enum as myEnum

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Unit(myEnum):
    ml = 'ml'
    tsp = 'tsp'
    dash = 'dash'
    drop = 'drop'
    pinch = 'pinch'
    Full_up = 'Full_up' # Full_up -> amount = 1
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
    unit = Column(Enum(Unit), nullable=False)
    amount = Column(Integer, nullable=False)
    cocktail_id = Column(Integer, ForeignKey('cocktail.id'), nullable=True)
    # cocktail = relationship("Cocktail", backref="materials")


class Cocktail(Base):
    __tablename__ = 'cocktail'

    id = Column(Integer, primary_key=True, )
    cocktail_name = Column(String, nullable=False)
    usage_count = Column(Integer, default=0)

    spirits = relationship("Spirit", cascade="all, delete", backref="cocktail")
    materials = relationship("Material", cascade="all, delete", backref="cocktail")
