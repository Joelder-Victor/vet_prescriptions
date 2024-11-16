from uuid import UUID
from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models.veterinarian import Veterinarian
from schemas.veterinarian import VeterinarianCreate, VeterinarianUpdate
from utils.images import upload_image_to_supabase
from utils.hashing import hash_password


def get_veterinarian(db: Session, veterinarian_id: str):
    return db.query(Veterinarian).filter(Veterinarian.email == veterinarian_id).first()


def get_veterinarians(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Veterinarian).offset(skip).limit(limit).all()


def update_veterinarian_logo(db: Session, veterinarian_email: str, logo_path: str):
    veterinarian = db.query(Veterinarian).filter(
        Veterinarian.email == veterinarian_email).first()
    if not veterinarian:
        raise Exception("Veterinarian not found")

    # Atualiza o campo logo_file
    upload_image_to_supabase(
        logo_path, f"logos/logo_{veterinarian.email}.png")

    veterinarian.logo_file = f"logos/logo_{veterinarian.email}.png"
    db.commit()
    db.refresh(veterinarian)
    return veterinarian


def update_veterinarian_signature(db: Session, veterinarian_email: str, signature_path: str):
    veterinarian = db.query(Veterinarian).filter(
        Veterinarian.email == veterinarian_email).first()
    if not veterinarian:
        raise Exception("Veterinarian not found")

    # Atualiza o campo signature_file
    upload_image_to_supabase(
        signature_path, f"signatures/signature_{veterinarian.email}.png")

    veterinarian.signature_file = f"signatures/signature_{veterinarian.email}.png"
    db.commit()
    db.refresh(veterinarian)
    return veterinarian


def create_veterinarian(db: Session, veterinarian: VeterinarianCreate):

    password = hash_password(veterinarian.password)

    db_veterinarian = Veterinarian(
        name=veterinarian.name,
        crmv=veterinarian.crmv,
        phone=veterinarian.phone,
        email=veterinarian.email,
        logo_file=veterinarian.logo_file,
        signature_file=veterinarian.signature_file,
        password=password
    )
    db.add(db_veterinarian)
    db.commit()
    db.refresh(db_veterinarian)

    return db_veterinarian


def update_veterinarian(db: Session, veterinarian_id: UUID, veterinarian: VeterinarianUpdate, logo_file: Optional[str] = None, signature_file: Optional[str] = None):
    db_veterinarian = db.query(Veterinarian).filter(
        Veterinarian.id == veterinarian_id).first()

    if db_veterinarian:
        if veterinarian.name:
            db_veterinarian.name = veterinarian.name
        if veterinarian.crmv:
            db_veterinarian.crmv = veterinarian.crmv
        if veterinarian.phone:
            db_veterinarian.phone = veterinarian.phone
        if veterinarian.email:
            db_veterinarian.email = veterinarian.email

        if logo_file:
            db_veterinarian.logo_file = upload_image_to_supabase(
                logo_file, f"logo_{veterinarian.name}.png")

        if signature_file:
            db_veterinarian.signature_file = upload_image_to_supabase(
                signature_file, f"signature_{veterinarian.name}.png")

        db.commit()
        db.refresh(db_veterinarian)
        return db_veterinarian
    return None


def delete_veterinarian(db: Session, veterinarian_id: UUID):
    db_veterinarian = get_veterinarian(db, veterinarian_id)
    if db_veterinarian:
        db.delete(db_veterinarian)
        db.commit()
    return db_veterinarian
