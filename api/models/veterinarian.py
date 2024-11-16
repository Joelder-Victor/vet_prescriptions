from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid
from database import Base


class Veterinarian(Base):
    __tablename__ = "veterinarian"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)
    name = Column(String, nullable=True)
    crmv = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    logo_file = Column(String, nullable=True)
    signature_file = Column(String, nullable=True)
    prescriptions_id = Column(ARRAY(UUID(as_uuid=True)), nullable=True)
    password = Column(String, nullable=True)
