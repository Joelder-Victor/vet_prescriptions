from uuid import UUID
from sqlalchemy.orm import Session
from models.animal import Animal
from schemas.animal import AnimalCreate

def get_animal(db: Session, animal_id: UUID):
    return db.query(Animal).filter(Animal.id == animal_id).first()

def get_animals(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Animal).offset(skip).limit(limit).all()

def create_animal(db: Session, animal: AnimalCreate):
    db_animal = Animal(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def update_animal(db: Session, animal_id: UUID, animal: AnimalCreate):
    db_animal = get_animal(db, animal_id)
    if db_animal:
        for key, value in animal.dict().items():
            setattr(db_animal, key, value)
        db.commit()
        db.refresh(db_animal)
    return db_animal

def delete_animal(db: Session, animal_id: UUID):
    db_animal = get_animal(db, animal_id)
    if db_animal:
        db.delete(db_animal)
        db.commit()
    return db_animal
