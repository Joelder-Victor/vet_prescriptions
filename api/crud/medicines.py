from uuid import UUID
from sqlalchemy.orm import Session
from models.medicines import Medicines
from schemas.medicines import MedicinesCreate


def get_medicine(db: Session, medicine_id: UUID):
    return db.query(Medicines).filter(Medicines.id == medicine_id).first()


def get_medicines(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Medicines).offset(skip).limit(limit).all()


def create_medicine(db: Session, medicine: MedicinesCreate):
    db_medicine = Medicines(**medicine.dict())
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine


def update_medicine(db: Session, medicine_id: UUID, medicine: MedicinesCreate):
    db_medicine = get_medicine(db, medicine_id)
    if db_medicine:
        for key, value in medicine.dict().items():
            setattr(db_medicine, key, value)
        db.commit()
        db.refresh(db_medicine)
    return db_medicine


def delete_medicine(db: Session, medicine_id: UUID):
    db_medicine = get_medicine(db, medicine_id)
    if db_medicine:
        db.delete(db_medicine)
        db.commit()
    return db_medicine
