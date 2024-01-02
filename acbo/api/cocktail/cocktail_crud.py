from sqlalchemy.orm import Session

from api.cocktail import cocktail_schema
from models import Cocktail


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
