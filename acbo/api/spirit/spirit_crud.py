from api.spirit.spirit_schema import SpiritCreate
from models import Spirit
from sqlalchemy.orm import Session


def get_spirit_list(db: Session):
    spirit_list = db.query(Spirit).order_by(Spirit.type.asc()).all()
    return spirit_list


def get_spirit(db: Session, spirit_id: int):
    spirit_detail = db.query(Spirit).get(spirit_id)
    return spirit_detail


def create_spirit(db: Session, spirit_create: SpiritCreate):
    db_spirit = Spirit(type=spirit_create.type,
                       measurement_id=spirit_create.measurement_id)
    db.add(db_spirit)
    db.commit()


def get_exist_spirit(db: Session, spirit_create: SpiritCreate):
    return db.query(Spirit).filter(Spirit.type == spirit_create.type,
                                   Spirit.measurement_id == spirit_create.measurement_id).first()
