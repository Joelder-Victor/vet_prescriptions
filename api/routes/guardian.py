from uuid import UUID
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from schemas.guardian import Guardian, GuardianCreate
from crud.guardian import create_guardian, get_guardian, get_guardians, update_guardian, delete_guardian

router = APIRouter(tags=["Guardians"])

# Dependência para a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/guardians/", response_model=Guardian)
def create_guardian_endpoint(guardian: GuardianCreate, db: Session = Depends(get_db)):
    return create_guardian(db=db, guardian=guardian)

@router.get("/guardians/", response_model=list[Guardian])
def read_guardians(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_guardians(db, skip=skip, limit=limit)

@router.get("/guardians/{guardian_id}", response_model=Guardian)
def read_guardian(guardian_id: UUID, db: Session = Depends(get_db)):
    db_guardian = get_guardian(db, guardian_id=guardian_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

@router.put("/guardians/{guardian_id}", response_model=Guardian)
def update_guardian_endpoint(guardian_id: UUID, guardian: GuardianCreate, db: Session = Depends(get_db)):
    db_guardian = update_guardian(db, guardian_id=guardian_id, guardian=guardian)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return db_guardian

@router.delete("/guardians/{guardian_id}")
def delete_guardian_endpoint(guardian_id: UUID, db: Session = Depends(get_db)):
    db_guardian = delete_guardian(db, guardian_id=guardian_id)
    if db_guardian is None:
        raise HTTPException(status_code=404, detail="Guardian not found")
    return {"message": "Guardian deleted successfully"}
