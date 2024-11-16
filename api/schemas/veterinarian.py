from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class VeterinarianBase(BaseModel):
    name: str = None
    crmv: str = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo_file: Optional[str] = None
    signature_file: Optional[str] = None
    prescriptions_id: Optional[List[UUID]] = None
    password: str


class VeterinarianCreate(VeterinarianBase):
    pass


class VeterinarianUpdate(VeterinarianBase):
    pass


class VeterinarianLogin(BaseModel):
    username: str
    password: str


class VeterinarianToken(BaseModel):
    id: UUID
    access_token: str
    token_type: str


class VeterinarianResponse(VeterinarianBase):
    id:UUID = None
    name: str = None
    crmv: str = None
    phone: Optional[str] = None
    email: Optional[str] = None
    logo_file: Optional[str] = None
    signature_file: Optional[str] = None
    prescriptions_id: Optional[List[UUID]] = None
    class Config:
        orm_mode = True

class Veterinarian(VeterinarianBase):
    id: UUID
    created_at: datetime
    password: str

    class Config:
        orm_mode = True
