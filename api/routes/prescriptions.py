from uuid import UUID
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from schemas.prescriptions import Prescriptions, PrescriptionsCreate
from crud.prescriptions import create_prescription, get_prescription, get_prescriptions, update_prescription, delete_prescription

router = APIRouter(tags=["Prescriptions"])

# Dependência para a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/prescriptions/", response_model=Prescriptions)
def create_prescription_endpoint(prescription: PrescriptionsCreate, db: Session = Depends(get_db)):
    return create_prescription(db=db, prescription=prescription)

@router.get("/prescriptions/", response_model=list[Prescriptions])
def read_prescriptions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_prescriptions(db, skip=skip, limit=limit)

@router.get("/prescriptions/{prescription_id}", response_model=Prescriptions)
def read_prescription(prescription_id: UUID, db: Session = Depends(get_db)):
    db_prescription = get_prescription(db, prescription_id=prescription_id)
    if db_prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return db_prescription

@router.put("/prescriptions/{prescription_id}", response_model=Prescriptions)
def update_prescription_endpoint(prescription_id: UUID, prescription: PrescriptionsCreate, db: Session = Depends(get_db)):
    db_prescription = update_prescription(db, prescription_id=prescription_id, prescription=prescription)
    if db_prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return db_prescription

@router.delete("/prescriptions/{prescription_id}")
def delete_prescription_endpoint(prescription_id: UUID, db: Session = Depends(get_db)):
    db_prescription = delete_prescription(db, prescription_id=prescription_id)
    if db_prescription is None:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return {"message": "Prescription deleted successfully"}
