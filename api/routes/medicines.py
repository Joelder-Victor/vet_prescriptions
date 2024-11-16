from uuid import UUID
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from schemas.medicines import Medicines, MedicinesCreate
from crud.medicines import create_medicine, get_medicine, get_medicines, update_medicine, delete_medicine

router = APIRouter(tags=["Medicines"])

# Dependência para a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/medicines/", response_model=Medicines)
def create_medicine_endpoint(medicine: MedicinesCreate, db: Session = Depends(get_db)):
    return create_medicine(db=db, medicine=medicine)

@router.get("/medicines/", response_model=list[Medicines])
def read_medicines(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_medicines(db, skip=skip, limit=limit)

@router.get("/medicines/{medicine_id}", response_model=Medicines)
def read_medicine(medicine_id: UUID, db: Session = Depends(get_db)):
    db_medicine = get_medicine(db, medicine_id=medicine_id)
    if db_medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return db_medicine

@router.put("/medicines/{medicine_id}", response_model=Medicines)
def update_medicine_endpoint(medicine_id: UUID, medicine: MedicinesCreate, db: Session = Depends(get_db)):
    db_medicine = update_medicine(db, medicine_id=medicine_id, medicine=medicine)
    if db_medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return db_medicine

@router.delete("/medicines/{medicine_id}")
def delete_medicine_endpoint(medicine_id: UUID, db: Session = Depends(get_db)):
    db_medicine = delete_medicine(db, medicine_id=medicine_id)
    if db_medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return {"message": "Medicine deleted successfully"}
