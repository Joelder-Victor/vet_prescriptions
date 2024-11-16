from sqlalchemy import Column, String, Float, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base

class Animal(Base):
    __tablename__ = "animal"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    name = Column(String, nullable=False)
    last_weight = Column(Float, nullable=True)
    breed = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    species = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    id_tutor = Column(UUID(as_uuid=True), ForeignKey("guardian.id"), nullable=True)
