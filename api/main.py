import os
from dotenv import load_dotenv

from fastapi import FastAPI
from routes import guardian, animal, medicines, prescriptions, veterinarian, login
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(openapi_prefix="/api/v1")
origins = [
    os.getenv("ORIGINS")
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas para guardians, animals, medicines, prescriptions e veterinarians
app.include_router(guardian.router, prefix="/api/v1")
app.include_router(animal.router, prefix="/api/v1")
app.include_router(medicines.router, prefix="/api/v1")
app.include_router(prescriptions.router, prefix="/api/v1")
app.include_router(veterinarian.router, prefix="/api/v1")
app.include_router(login.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "VetOne is live!!"}