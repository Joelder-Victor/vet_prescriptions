import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")


def register_guardian(name, address, animals_id=[]):
    """
    Registra um novo tutor no sistema.

    """
    response = requests.post(f"{API_URL}/guardians", json={
        "name": name,
        "address": address,
        "animals_id": animals_id
    })
    if response.status_code == 200:
        print("Cadastro realizado com sucesso!")
        return response.json().get("id")
    else:
        print("Erro ao cadastrar: " +
              response.json().get("detail", "Erro desconhecido"))


def register_animal(name, weight, breed, gender, species, age, tutor_id):
    """
    Registra um novo tutor no sistema.

    """
    response = requests.post(f"{API_URL}/animals", json={
        "name": name,
        "last_weight": weight,
        "breed": breed,
        "gender": gender,
        "species": species,
        "age": age,
        "id_tutor": tutor_id
    })
    if response.status_code == 200:
        print("Cadastro realizado com sucesso!")
        return response.json().get("id")
    else:
        print("Erro ao cadastrar: " +
              response.json().get("detail", "Erro desconhecido"))
