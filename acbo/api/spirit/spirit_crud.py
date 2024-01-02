from sqlalchemy.orm import Session

from api.spirit import spirit_schema
from models import Spirit


def get_spirit_list(db: Session):
    _spirit_list = db.query(Spirit).order_by(Spirit.type.asc())
    total, spirit_list = _spirit_list.count(), _spirit_list.all()
    return total, spirit_list


def get_spirit(db: Session, spirit_id: int):
    spirit_detail = db.query(Spirit).get(spirit_id)
    return spirit_detail


def get_exist_spirit(db: Session, spirit: spirit_schema.SpiritCreate | spirit_schema.SpiritUpdate):
    return db.query(Spirit).filter(Spirit.type == spirit.type,
                                   Spirit.unit == spirit.unit,
                                   Spirit.amount == spirit.amount).first()


def create_spirit(db: Session, spirit: spirit_schema.SpiritCreate):
    db_spirit = Spirit(type=spirit.type,
                       unit=spirit.unit,
                       amount=spirit.amount,
                       cocktail_id=spirit.cocktail_id)
    db.add(db_spirit)
    db.commit()


def delete_spirit(db: Session, spirit_id: int):
    spirit_delete = db.query(Spirit).filter(Spirit.id == spirit_id).first()
    db.delete(spirit_delete)
    db.commit()



def update_spirit(db: Session,
                  db_spirit: Spirit,
                  spirit_update: spirit_schema.SpiritUpdate):
    db_spirit.type = spirit_update.type
    db_spirit.unit = spirit_update.unit
    db_spirit.amount = spirit_update.amount
    db.add(db_spirit)
    db.commit()
