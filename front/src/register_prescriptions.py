import streamlit as st
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")


def register_medicine(name,quant,dosage,prescription=None):

    """
    Registra um novo medicamento no sistema.

    """
    response = requests.post(f"{API_URL}/medicines", json={
        "name": name,
        "quantity":quant,
        "dosage":dosage,
        "prescription_id":prescription
    })
    if response.status_code == 200:
        print("Cadastro realizado com sucesso!")
        return response.json().get("id")
    else:
        print("Erro ao cadastrar: " +
              
              response.json().get("detail", "Erro desconhecido"))

def register_prescription(id_vet,id_tutor,id_animal,medicines_ids=[]):

    """
    Registra um novo medicamento no sistema.

    """
    response = requests.post(f"{API_URL}/prescriptions", json={
        "id_vet":id_vet,
        "id_tutor":id_tutor,
        "id_animal":id_animal,
        "medicines_id":medicines_ids
    })
    if response.status_code == 200:
        print("Cadastro realizado com sucesso!")
        return response.json().get("id")
    else:
        print("Erro ao cadastrar: " +
              response.json().get("detail", "Erro desconhecido"))
