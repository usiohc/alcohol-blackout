from sqlalchemy import func, distinct, select
from sqlalchemy.orm import Session

from api.material import material_schema
from models import Material, Spirit


def get_material_list(db: Session):
    _material_list = db.query(Material).order_by(Material.id.asc())
    total, material_list = _material_list.count(), _material_list.all()
    return total, material_list


def get_material(db: Session, material_id: int):
    material_detail = db.query(Material).get(material_id)
    return material_detail


def get_exist_material(db: Session, material: material_schema.MaterialCreate):
    return db.query(Material).filter(Material.type == material.type,
                                     Material.name == material.name,
                                     Material.unit == material.unit,
                                     Material.amount == material.amount,
                                     Material.cocktail_id == material.cocktail_id).first()


def create_material(db: Session, material: material_schema.MaterialCreate):
    db_material = Material(type=material.type,
                           name=material.name,
                           unit=material.unit,
                           amount=material.amount,
                           cocktail_id=material.cocktail_id)
    db.add(db_material)
    db.commit()


def delete_material(db: Session, material_id: int):
    material_delete = db.query(Material).filter(Material.id == material_id).first()
    db.delete(material_delete)
    db.commit()


def update_material(db: Session,
                    db_material: Material,
                    material_update: material_schema.MaterialUpdate):
    db_material.type = material_update.type
    db_material.name = material_update.name
    db_material.unit = material_update.unit
    db_material.amount = material_update.amount
    db.add(db_material)
    db.commit()


def get_material_by_spirits(db: Session,
                            spirit_type: list):
    query = db.query(Material.type, Material.name)

    if spirit_type:
        # 서브 쿼리: Spirit 테이블에서 SpiritType에 해당하는 cocktail_id를 가져옴
        subquery = db.query(Spirit.cocktail_id)\
            .filter(Spirit.type.in_(spirit_type))\
            .group_by(Spirit.cocktail_id)\
            .having(func.count(Spirit.type) == len(spirit_type))

        # 메인 쿼리: Material 테이블에서 서브쿼리의 cocktail_id에 해당하는 type, name을 가져옴 | Groupby 로 중복 제거
        query = query.filter(Material.cocktail_id.in_(subquery))\
                     .group_by(Material.type, Material.name)
    else: # spirit_type이 없으면 모든 type, name 반환
        query = query.group_by(Material.type, Material.name)

    # 쿼리 실행 및 결과 반환
    total, results = query.count(), query.all()
    materials = [{"type": str(row.type.value), "name": row.name} for row in results]

    return total, materials
