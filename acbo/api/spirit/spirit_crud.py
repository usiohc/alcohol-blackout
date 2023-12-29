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


def create_spirit(db: Session, spirit: spirit_schema.SpiritCreate):
    db_spirit = Spirit(type=spirit.type,
                       measurement_id=spirit.measurement.id)
    db.add(db_spirit)
    db.commit()


def get_exist_spirit(db: Session, spirit: spirit_schema.SpiritCreate):
    return db.query(Spirit).filter(Spirit.type == spirit.type,
                                   Spirit.measurement_id == spirit.measurement.id).first()


def delete_spirit(db: Session, spirit_id: int):
    if spirit_delete := db.query(Spirit).filter(Spirit.id == spirit_id).first():
        db.delete(spirit_delete)
        db.commit()
        return True
    else:
        return False
