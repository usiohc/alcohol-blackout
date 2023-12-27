from sqlalchemy.orm import Session

from api.measurement import measurement_schema
from models import Measurement


def get_measurement_list(db: Session):
    measurement_list = db.query(Measurement).order_by(Measurement.id.asc()).all()
    return measurement_list


def get_measurement(db: Session, measurement_id: int):
    measurement_detail = db.query(Measurement).get(measurement_id)
    return measurement_detail


def create_measurement(db: Session, _measurement_create: measurement_schema.MeasurementCreate):
    db_measurement = Measurement(unit=_measurement_create.unit,
                                 amount=_measurement_create.amount)
    db.add(db_measurement)
    db.commit()
    return db_measurement


def get_exist_measurement(db: Session, _measurement: measurement_schema.MeasurementCreate):
    return db.query(Measurement).filter(Measurement.unit == _measurement.unit,
                                        Measurement.amount == _measurement.amount).first()
