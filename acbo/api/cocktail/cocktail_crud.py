from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from api.cocktail import cocktail_schema
from models import Cocktail, Material, Spirit


def get_cocktail_list(db: Session):
    cocktail_list = db.query(Cocktail).order_by(Cocktail.name.asc()).all()
    return len(cocktail_list), cocktail_list


def get_cocktail(db: Session, cocktail_id: int):
    return db.query(Cocktail).get(cocktail_id)


def get_cocktail_spirit_list(db: Session, cocktail_id: int):
    cocktail_spirit_list = db.query(Cocktail).get(cocktail_id).spirits
    return len(cocktail_spirit_list), cocktail_spirit_list


def get_cocktail_material_list(db: Session, cocktail_id: int):
    cocktail_material_list = db.query(Cocktail).get(cocktail_id).materials
    return len(cocktail_material_list), cocktail_material_list


def create_cocktail(db: Session, cocktail: cocktail_schema.CocktailCreate):
    db_cocktail = Cocktail(**cocktail.model_dump())
    db.add(db_cocktail)
    db.commit()
    db.refresh(db_cocktail)
    return db_cocktail


def update_cocktail(
    db: Session, db_cocktail: Cocktail, cocktail_update: cocktail_schema.CocktailUpdate
):
    for key, value in cocktail_update.model_dump().items():
        setattr(db_cocktail, key, value)
    db.add(db_cocktail)
    db.commit()
    db.refresh(db_cocktail)
    return db_cocktail


def delete_cocktail(db: Session, cocktail_id: int):
    cocktail_delete = db.query(Cocktail).get(cocktail_id)
    db.delete(cocktail_delete)
    db.commit()


def get_cocktail_by_spirit_material(db: Session, spirits: list, materials: list):
    if spirits:
        # 서브 쿼리:
        subquery = (
            db.query(Spirit.cocktail_id)
            .filter(Spirit.type.in_(spirits))
            .group_by(Spirit.cocktail_id)
            .having(func.count(Spirit.type) == len(spirits))
        )
        # 메인 쿼리:
        spirits = (
            db.query(Spirit.cocktail_id).filter(Spirit.cocktail_id.in_(subquery)).all()
        )
    else:  # spirits 이 없으면 모든 cocktail_id 반환
        spirits = db.query(Cocktail.id).all()

    # spirits = [(1,), ...] | [] -> result = (1, ...) | ()
    result = set(map(lambda x: x[0], spirits))

    if materials:
        for material_type, material_name in materials:
            _materials = (
                db.query(Material.cocktail_id)
                .filter(
                    and_(Material.type == material_type, Material.name == material_name)
                )
                .group_by(Material.cocktail_id)
                .all()
            )
            result = result & set(
                map(lambda x: x[0], _materials)
            )  # _materials = [(1,), ...]

    cocktails = (
        db.query(Cocktail)
        .filter(Cocktail.id.in_(result))
        .order_by(Cocktail.name_ko.asc(), Cocktail.name.asc())
        .all()
    )

    return len(cocktails), cocktails


def get_cocktail_detail_by_name(db: Session, cocktail_name: str):
    return db.query(Cocktail).filter(Cocktail.name == cocktail_name).first()
