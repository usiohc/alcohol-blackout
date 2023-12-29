from sqlalchemy.orm import Session

from api.measurement import measurement_schema
from models import Measurement


def get_measurement_list(db: Session):
    _measurement_list = (db.query(Measurement).order_by(Measurement.id.asc()))
    total, measurement_list = _measurement_list.count(), _measurement_list.all()
    return total, measurement_list


def get_measurement(db: Session, measurement_id: int):
    measurement_detail = db.query(Measurement).get(measurement_id)
    return measurement_detail


def create_measurement(db: Session, measurement_create: measurement_schema.MeasurementCreate):
    db_measurement = Measurement(unit=measurement_create.unit,
                                 amount=measurement_create.amount)
    db.add(db_measurement)
    db.commit()
    return db_measurement


def get_exist_measurement(db: Session, measurement: measurement_schema.MeasurementCreate):
    return db.query(Measurement).filter(Measurement.unit == measurement.unit,
                                        Measurement.amount == measurement.amount).first()


def delete_measurement(db: Session, measurement_id: Measurement.id):
    if measurement_delete := db.query(Measurement).filter(Measurement.id == measurement_id).first():
        db.delete(measurement_delete)
        db.commit()
        return True
    else:
        return False
