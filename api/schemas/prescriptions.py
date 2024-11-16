from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class PrescriptionsBase(BaseModel):
    id_vet: Optional[UUID] = None
    id_tutor: Optional[UUID] = None
    id_animal: Optional[UUID] = None
    medicines_id: Optional[List[UUID]] = None

class PrescriptionsCreate(PrescriptionsBase):
    pass

class Prescriptions(PrescriptionsBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
