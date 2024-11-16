from uuid import UUID
from pathlib import Path
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Depends, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from utils.auth import verify_token, oauth2_scheme

from schemas.veterinarian import Veterinarian, VeterinarianCreate, VeterinarianUpdate, VeterinarianResponse
from crud.veterinarian import create_veterinarian, get_veterinarian, get_veterinarians, update_veterinarian
from crud.veterinarian import delete_veterinarian, update_veterinarian_logo, update_veterinarian_signature
from utils.images import download_image_from_supabase

router = APIRouter(tags=["Veterinarian"])

# Dependência para a sessão do banco de dados
UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_veterinarian(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    veterinarian_id = payload.get("username")
    if veterinarian_id is None:
        raise credentials_exception
    veterinarian = get_veterinarian(db, veterinarian_id)
    if veterinarian is None:
        raise credentials_exception
    return veterinarian


@router.post("/veterinarian/{veterinarian_email}/upload-logo", response_model=VeterinarianResponse)
async def upload_logo(
    veterinarian_email: str,
    logo: UploadFile,
    db: Session = Depends(get_db),
    current_veterinarian: Veterinarian = Depends(get_current_veterinarian)
):

    if current_veterinarian.email != veterinarian_email:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this veterinarian's information"
        )
    # Define o caminho do arquivo logo
    logo_file_path = UPLOAD_DIR / f"logo_{veterinarian_email}.png"

    # Salva o arquivo logo no diretório
    with open(logo_file_path, "wb") as file:
        file.write(await logo.read())

    # Atualiza o caminho do logo no banco de dados
    try:
        updated_veterinarian = update_veterinarian_logo(
            db, veterinarian_email, str(logo_file_path)
        )
        return JSONResponse(status_code=200, content={"detail": "Upload com sucesso"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/veterinarian/{veterinarian_email}/upload-signature", response_model=VeterinarianResponse)
async def upload_signature(
    veterinarian_email: str,
    signature: UploadFile,
    db: Session = Depends(get_db),
    current_veterinarian: Veterinarian = Depends(get_current_veterinarian)
):
    if current_veterinarian.email != veterinarian_email:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this veterinarian's information"
        )
    # Define o caminho do arquivo signature
    signature_file_path = UPLOAD_DIR / f"signature_{veterinarian_email}.png"

    # Salva o arquivo signature no diretório
    with open(signature_file_path, "wb") as file:
        file.write(await signature.read())

    # Atualiza o caminho do signature no banco de dados
    try:
        updated_veterinarian = update_veterinarian_signature(
            db, veterinarian_email, str(signature_file_path)
        )
        return {"message": "signature uploaded successfully", "data": updated_veterinarian}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/veterinarian/", response_model=Veterinarian)
def create_veterinarian_route(veterinarian: VeterinarianCreate, db: Session = Depends(get_db)):

    try:
        return create_veterinarian(db, veterinarian)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# @ router.get("/veterinarians/", response_model=list[Veterinarian])
# def read_veterinarians(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return get_veterinarians(db, skip=skip, limit=limit)

@router.get("/veterinarian/{veterinarian_email}/get-logo")
async def get_logo(
    veterinarian_email: str,
    # db: Session = Depends(get_db),
    current_veterinarian: Veterinarian = Depends(get_current_veterinarian)
):
    # Verifica se o usuário autenticado tem permissão
    if current_veterinarian.email != veterinarian_email:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this veterinarian's information"
        )

    # Obtém o veterinário e verifica se o logo está disponível
    object_key = f"logo_{veterinarian_email}.png"
    download_image_from_supabase(
        object_key, DOWNLOAD_DIR, "logos/"+object_key)

    logo_path = f"{DOWNLOAD_DIR}/logo_{veterinarian_email}.png"

    # Retorna o logo como resposta

    return FileResponse(logo_path, media_type="image/png", filename=f"logo_{veterinarian_email}.png")


@router.get("/veterinarian/{veterinarian_email}/get-signature")
async def get_signature(
    veterinarian_email: str,
    # db: Session = Depends(get_db),
    current_veterinarian: Veterinarian = Depends(get_current_veterinarian)
):
    # Verifica se o usuário autenticado tem permissão
    if current_veterinarian.email != veterinarian_email:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this veterinarian's information"
        )

    # Obtém o veterinário e verifica se o signature está disponível
    object_key = f"signature_{veterinarian_email}.png"
    download_image_from_supabase(
        object_key, DOWNLOAD_DIR, "signatures/"+object_key)

    signature_path = f"{DOWNLOAD_DIR}/signature_{veterinarian_email}.png"

    # Retorna o signature como resposta

    return FileResponse(signature_path, media_type="image/png", filename=f"signature_{veterinarian_email}.png")


@ router.get("/veterinarians/{veterinarian_email}", response_model=VeterinarianResponse)
def read_veterinarian(veterinarian_email: str,
                      db: Session = Depends(get_db),
                      current_veterinarian: Veterinarian = Depends(get_current_veterinarian)):
    if current_veterinarian.email != veterinarian_email:
        raise HTTPException(
            status_code=403,  # Forbidden
            detail="You do not have permission to access this veterinarian's information"
        )

    db_veterinarian = get_veterinarian(db, veterinarian_id=veterinarian_email)
    if db_veterinarian is None:
        raise HTTPException(status_code=404, detail="Veterinarian not found")
    return db_veterinarian


@ router.put("/veterinarian/{veterinarian_id}", response_model=Veterinarian)
def update_veterinarian_route(veterinarian_id: UUID, veterinarian: VeterinarianUpdate, db: Session = Depends(get_db)):

    return update_veterinarian(db, veterinarian_id, veterinarian)


@ router.delete("/veterinarians/{veterinarian_id}")
def delete_veterinarian_endpoint(veterinarian_id: UUID, db: Session = Depends(get_db)):
    db_veterinarian = delete_veterinarian(db, veterinarian_id=veterinarian_id)
    if db_veterinarian is None:
        raise HTTPException(status_code=404, detail="Veterinarian not found")
    return {"message": "Veterinarian deleted successfully"}
