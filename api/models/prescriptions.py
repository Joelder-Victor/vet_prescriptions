from sqlalchemy import Column, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid
from database import Base

class Prescriptions(Base):
    __tablename__ = "prescriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    id_vet = Column(UUID(as_uuid=True), ForeignKey("veterinarian.id"), nullable=True)
    id_tutor = Column(UUID(as_uuid=True), ForeignKey("guardian.id"), nullable=True)
    id_animal = Column(UUID(as_uuid=True), ForeignKey("animal.id"), nullable=True)
    medicines_id = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
