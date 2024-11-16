from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import SessionLocal
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models.veterinarian import Veterinarian  # Importa o modelo
from schemas.veterinarian import VeterinarianLogin, VeterinarianToken  # Esquema de login
from utils.hashing import verify_password

from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(tags=["Login"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=VeterinarianToken)
async def login(veterinarian: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_veterinarian = db.query(Veterinarian).filter(
        Veterinarian.email == veterinarian.username).first()

    if not db_veterinarian or not verify_password(veterinarian.password, db_veterinarian.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )

    # Cria o token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": db_veterinarian.email}, expires_delta=access_token_expires
    )
    vet = VeterinarianToken(
        id=db_veterinarian.id,
        access_token=access_token,
        token_type="bearer"
    )
    return vet
