from uuid import UUID
from sqlalchemy.orm import Session
from models.prescriptions import Prescriptions
from schemas.prescriptions import PrescriptionsCreate

def get_prescription(db: Session, prescription_id: UUID):
    return db.query(Prescriptions).filter(Prescriptions.id == prescription_id).first()

def get_prescriptions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Prescriptions).offset(skip).limit(limit).all()

def create_prescription(db: Session, prescription: PrescriptionsCreate):
    db_prescription = Prescriptions(**prescription.dict())
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def update_prescription(db: Session, prescription_id: UUID, prescription: PrescriptionsCreate):
    db_prescription = get_prescription(db, prescription_id)
    if db_prescription:
        for key, value in prescription.dict().items():
            setattr(db_prescription, key, value)
        db.commit()
        db.refresh(db_prescription)
    return db_prescription

def delete_prescription(db: Session, prescription_id: UUID):
    db_prescription = get_prescription(db, prescription_id)
    if db_prescription:
        db.delete(db_prescription)
        db.commit()
    return db_prescription
