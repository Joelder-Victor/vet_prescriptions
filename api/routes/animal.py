from uuid import UUID
from database import SessionLocal
from sqlalchemy.orm import Session
from schemas.animal import Animal, AnimalCreate
from fastapi import APIRouter, Depends, HTTPException
from crud.animal import create_animal, get_animal, get_animals, update_animal, delete_animal

router = APIRouter(tags=["Animal"])

# Dependência para a sessão do banco de dados


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/animals/", response_model=Animal)
def create_animal_route(animal: AnimalCreate, db: Session = Depends(get_db)):
    return create_animal(db=db, animal=animal)


@router.get("/animals/", response_model=list[Animal])
def read_animals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_animals(db, skip=skip, limit=limit)


@router.get("/animals/{animal_id}", response_model=Animal)
def read_animal(animal_id: UUID, db: Session = Depends(get_db)):
    db_animal = get_animal(db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return db_animal


@router.put("/animals/{animal_id}", response_model=Animal)
def update_animal(animal_id: UUID, animal: AnimalCreate, db: Session = Depends(get_db)):
    db_animal = update_animal(db, animal_id=animal_id, animal=animal)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return db_animal


@router.delete("/animals/{animal_id}")
def delete_animal(animal_id: UUID, db: Session = Depends(get_db)):
    db_animal = delete_animal(db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {"message": "Animal deleted successfully"}
