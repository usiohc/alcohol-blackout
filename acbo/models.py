from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as myEnum

from database import Base


class Unit(myEnum):
    ml = 'ml'
    tsp = 'tsp'
    dash = 'dash'
    drop = 'drop'
    pinch = 'pinch'
    Full_up = 'Full_up'
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
    Base = 'Base'
    Syrup = 'Syrup'
    Juice = 'Juice'
    Soda = 'Soda'
    Garnish = 'Garnish'


class Measurement(Base):
    __tablename__ = 'measurement'

    id = Column(Integer, primary_key=True)
    unit = Column(Enum(Unit))
    amount = Column(Integer, nullable=False)


class Spirit(Base):
    __tablename__ = 'spirit'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(SpiritType))
    measurement_id = Column(Integer, ForeignKey('measurement.id'))
    usage_count = Column(Integer, default=0)

    measurement = relationship("Measurement")


class Material(Base):
    __tablename__ = 'material'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(MaterialType))
    name = Column(String, nullable=False)
    measurement_id = Column(Integer, ForeignKey('measurement.id'))
    usage_count = Column(Integer, default=0)

    measurement = relationship("Measurement")


class Cocktail(Base):
    __tablename__ = 'cocktail'

    id = Column(Integer, primary_key=True)
    spirit_id = Column(Integer, ForeignKey('spirit.id'))
    cocktail_name = Column(String, nullable=False)
    usage_count = Column(Integer, default=0)

    spirit = relationship("Spirit")


class CocktailIngredient(Base):
    __tablename__ = 'cocktail_ingredient'

    id = Column(Integer, primary_key=True)
    cocktail_id = Column(Integer, ForeignKey('cocktail.id'))
    material_id = Column(Integer, ForeignKey('material.id'))

    cocktail = relationship("Cocktail")
    material = relationship("Material")
