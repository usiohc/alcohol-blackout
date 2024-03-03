from enum import Enum as myEnum


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
    Full_up = 'Full_up'  # Full_up -> amount = 0
    piece = 'piece'


class SpiritType(myEnum):
    Vodka = 'Vodka'
    Gin = 'Gin'
    Rum = 'Rum'
    Tequila = 'Tequila'
    Whisky = 'Whisky'
    Brandy = 'Brandy'
    Wine = 'Wine'


class MaterialType(myEnum):
    Liqueur = 'Liqueur'
    Syrup = 'Syrup'
    Juice = 'Juice'
    Soda = 'Soda'
    Garnish = 'Garnish'
    Etc = 'Etc'
