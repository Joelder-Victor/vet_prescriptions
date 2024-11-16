from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class GuardianBase(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    animals_id: Optional[List[UUID]] = None

class GuardianCreate(GuardianBase):
    pass

class Guardian(GuardianBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
