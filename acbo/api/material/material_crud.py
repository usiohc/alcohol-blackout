from sqlalchemy import func
from sqlalchemy.orm import Session

from api.material import material_schema
from models import Material, Spirit


def get_material_list(db: Session):
    material_list = db.query(Material).order_by(Material.type.asc(), Material.name_ko.asc(), Material.name.asc()).all()
    return len(material_list), material_list


def get_material(db: Session, material_id: int):
    return db.query(Material).get(material_id)


def create_material(db: Session, material: material_schema.MaterialCreate):
    db_material = Material(**material.model_dump())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def update_material(db: Session,
                    db_material: Material,
                    material_update: material_schema.MaterialUpdate):
    for key, value in material_update.model_dump().items():
        setattr(db_material, key, value)
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def delete_material(db: Session, material_id: int):
    material_delete = db.query(Material).get(material_id)
    db.delete(material_delete)
    db.commit()


def get_material_by_spirit(db: Session,
                           spirits: list):
    # TODO: 재료가 많아지면 Material 테이블의 type, name, name_ko 정규화 필요 -> 새로운 테이블 Material_Ingredient 생성 필요
    if spirits:  # Spirit 테이블에서 SpiritType에 해당하는 cocktail_id를 가져옴
        spirits = db.query(Spirit.cocktail_id) \
                    .filter(Spirit.type.in_(spirits)) \
                    .group_by(Spirit.cocktail_id) \
                    .having(func.count(Spirit.type) == len(spirits)).all()
    else:  # spirit_type이 없으면 모든 type, name 반환 (Frontend 에서 기주 선택 X)
        spirits = db.query(Spirit.id).distinct().all()

    result = set(map(lambda x: x[0], spirits))

    # sqlalchemy event.listen(load)는 테이블의 속성을 쿼리하면 동작 X
    materials = db.query(Material.type, Material.name, Material.name_ko).distinct() \
                  .filter(Material.cocktail_id.in_(result)) \
                  .order_by(Material.type.asc(), Material.name_ko.asc(), Material.name.asc()).all()

    # event listener 동작 X, 수동으로 replace 해야함
    materials = [material_schema.MaterialOmittedUnitAmount(
        type=material.type.value,
        name=material.name.replace("_", " "),
        name_ko=material.name_ko.replace("_", " ")) for material in materials]

    return len(materials), materials
