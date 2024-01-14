from sqlalchemy import and_, union, tuple_, func
from sqlalchemy.orm import Session

from api.cocktail import cocktail_schema
from models import Cocktail, Material, Spirit


def get_cocktail_list(db: Session):
    _cocktail_list = db.query(Cocktail).order_by(Cocktail.name.asc())
    total, cocktail_list = _cocktail_list.count(), _cocktail_list.all()
    return total, cocktail_list


def get_cocktail(db: Session, cocktail_id: int):
    cocktail_detail = db.query(Cocktail).get(cocktail_id)
    return cocktail_detail


def get_cocktail_spirit_list(db: Session, cocktail_id: int):
    cocktail_spirit_list = db.query(Cocktail).get(cocktail_id).spirits
    total = len(cocktail_spirit_list)
    return total, cocktail_spirit_list


def get_cocktail_material_list(db: Session, cocktail_id: int):
    cocktail_material_list = db.query(Cocktail).get(cocktail_id).materials
    total = len(cocktail_material_list)
    return total, cocktail_material_list


def get_exist_cocktail(db: Session, cocktail: cocktail_schema.CocktailCreate | cocktail_schema.CocktailUpdate):
    return db.query(Cocktail).filter(Cocktail.name == cocktail.name).first()


def create_cocktail(db: Session, cocktail: cocktail_schema.CocktailCreate):
    db_cocktail = Cocktail(name=cocktail.name)
    db.add(db_cocktail)
    db.commit()

def delete_cocktail(db: Session, cocktail_id: int):
    cocktail_delete = db.query(Cocktail).filter(Cocktail.id == cocktail_id).first()
    db.delete(cocktail_delete)
    db.commit()


def update_cocktail(db: Session,
                    db_cocktail: Cocktail,
                    cocktail_update: cocktail_schema.CocktailUpdate):
    db_cocktail.name = cocktail_update.name
    db.add(db_cocktail)
    db.commit()


def get_cocktail_by_spirit_material(spirits: list,
                                    materials: list | None,
                                    db: Session):
    if spirits:
        # 서브 쿼리:
        subquery = db.query(Spirit.cocktail_id)\
                     .filter(Spirit.type.in_(spirits))\
                     .group_by(Spirit.cocktail_id)\
                     .having(func.count(Spirit.type) == len(spirits))

        # 메인 쿼리:
        spirits = db.query(Spirit.cocktail_id).filter(Spirit.cocktail_id.in_(subquery))\
                    .group_by(Spirit.cocktail_id).all()
    else: # spirits 이 없으면 모든 cocktail_id 반환
        spirits = db.query(Cocktail.id).all()

    result = set(spirit[0] for spirit in spirits)

    if materials:
        for material_type, material_name in materials:
            subquery = db.query(Material.cocktail_id)\
                .filter(and_(Material.type == material_type, Material.name == material_name))\
                .group_by(Material.cocktail_id).all()
            result = result & set(material[0] for material in subquery) # subquery = [(1,), ...]

    query = db.query(Cocktail).filter(Cocktail.id.in_(result)).order_by(Cocktail.usage_count.desc())
    total, cocktails = query.count(), query.all()
    for cocktail in cocktails:
        cocktail.name = cocktail.name.replace("_", " ")

    return total, cocktails


def get_cocktail_by_name(db: Session, name: str):
    cocktail_detail = db.query(Cocktail).filter(Cocktail.name == name).first()
    if cocktail_detail:
        cocktail_detail.usage_count += 1
        db.add(cocktail_detail)
        db.commit()

        cocktail_detail.name = cocktail_detail.name.replace("_", " ")
        for material in cocktail_detail.materials:
            material.name = material.name.replace("_", " ")

    return cocktail_detail
