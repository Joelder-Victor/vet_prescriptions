from sqlalchemy import Column, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid
from database import Base

class Guardian(Base):
    __tablename__ = "guardian"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    animals_id = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
