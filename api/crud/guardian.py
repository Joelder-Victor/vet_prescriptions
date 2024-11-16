from uuid import UUID
from sqlalchemy.orm import Session
from models.guardian import Guardian
from schemas.guardian import GuardianCreate

def get_guardian(db: Session, guardian_id: UUID):
    return db.query(Guardian).filter(Guardian.id == guardian_id).first()

def get_guardians(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Guardian).offset(skip).limit(limit).all()

def create_guardian(db: Session, guardian: GuardianCreate):
    db_guardian = Guardian(**guardian.dict())
    db.add(db_guardian)
    db.commit()
    db.refresh(db_guardian)
    return db_guardian

def update_guardian(db: Session, guardian_id: UUID, guardian: GuardianCreate):
    db_guardian = get_guardian(db, guardian_id)
    if db_guardian:
        for key, value in guardian.dict().items():
            setattr(db_guardian, key, value)
        db.commit()
        db.refresh(db_guardian)
    return db_guardian

def delete_guardian(db: Session, guardian_id: UUID):
    db_guardian = get_guardian(db, guardian_id)
    if db_guardian:
        db.delete(db_guardian)
        db.commit()
    return db_guardian
