from sqlalchemy.orm import Session

from api.spirit import spirit_schema
from models import Spirit


def get_spirit_list(db: Session):
    spirit_list = db.query(Spirit).order_by(Spirit.type.asc()).all()
    return spirit_list


def get_spirit(db: Session, spirit_id: int):
    spirit_detail = db.query(Spirit).get(spirit_id)
    return spirit_detail


def create_spirit(db: Session, _spirit: spirit_schema.SpiritCreate):
    db_spirit = Spirit(type=_spirit.type,
                       measurement_id=_spirit.measurement.id)
    db.add(db_spirit)
    db.commit()


def get_exist_spirit(db: Session, _spirit: spirit_schema.SpiritCreate):
    return db.query(Spirit).filter(Spirit.type == _spirit.type,
                                   Spirit.measurement_id == _spirit.measurement.id).first()
