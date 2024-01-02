from sqlalchemy.orm import Session

from api.material import material_schema
from models import Material


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
                                     Material.amount == material.amount).first()


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
