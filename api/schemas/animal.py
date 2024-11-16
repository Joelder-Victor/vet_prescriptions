from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class AnimalBase(BaseModel):
    name: str
    last_weight: Optional[float] = None
    breed: Optional[str] = None
    gender: Optional[str] = None
    species: Optional[str] = None
    age: Optional[int] = None
    id_tutor: Optional[UUID] = None

class AnimalCreate(AnimalBase):
    pass

class Animal(AnimalBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
