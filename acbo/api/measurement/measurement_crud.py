from api.measurement.measurement_schema import MeasurementCreate
from models import Measurement
from sqlalchemy.orm import Session


def get_measurement_list(db: Session):
    measurement_list = db.query(Measurement).order_by(Measurement.id.asc()).all()
    return measurement_list


def get_measurement(db: Session, measurement_id: int):
    measurement_detail = db.query(Measurement).get(measurement_id)
    return measurement_detail


def create_measurement(db: Session, measurement_create: MeasurementCreate):
    db_measurement = Measurement(unit=measurement_create.unit,
                                 amount=measurement_create.amount)
    db.add(db_measurement)
    db.commit()
    return db_measurement


def get_exist_measurement(db: Session, measurement_create: MeasurementCreate):
    return db.query(Measurement).filter(Measurement.unit == measurement_create.unit,
                                        Measurement.amount == measurement_create.amount).first()
