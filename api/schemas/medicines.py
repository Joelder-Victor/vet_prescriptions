from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class MedicinesBase(BaseModel):
    name: Optional[str] = None
    quantity: Optional[str] = None
    dosage: Optional[str] = None
    prescription_id: Optional[UUID] = None

class MedicinesCreate(MedicinesBase):
    pass

class Medicines(MedicinesBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
