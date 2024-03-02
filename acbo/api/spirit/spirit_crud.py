from sqlalchemy.orm import Session

from api.spirit import spirit_schema
from models import Spirit


def get_spirit_list(db: Session):
    spirit_list = db.query(Spirit).order_by(Spirit.type.asc(), Spirit.name.asc()).all()
    return len(spirit_list), spirit_list


def get_spirit(db: Session, spirit_id: int):
    return db.query(Spirit).get(spirit_id)

def create_spirit(db: Session, spirit: spirit_schema.SpiritCreate):
    db_spirit = Spirit(**spirit.model_dump())
    db.add(db_spirit)
    db.commit()
    db.refresh(db_spirit)
    return db_spirit


def update_spirit(db: Session,
                  db_spirit: Spirit,
                  spirit_update: spirit_schema.SpiritUpdate):
    for key, value in spirit_update.model_dump().items():
        setattr(db_spirit, key, value)
    db.add(db_spirit)
    db.commit()
    db.refresh(db_spirit)
    return db_spirit


def delete_spirit(db: Session, spirit_id: int):
    spirit_delete = db.query(Spirit).get(spirit_id)
    db.delete(spirit_delete)
    db.commit()
