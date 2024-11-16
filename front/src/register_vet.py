from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
import streamlit as st
import requests
from pathlib import Path
import os
import requests
from dotenv import load_dotenv

load_dotenv()


API_URL = os.getenv("API_URL")

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def upload_logo(file, email, token):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    print(file.name)
    files = {
        'logo': (file.name, file, 'image/png')
    }

    response = requests.post(
        f"{API_URL}/veterinarians/{email}/upload-logo", headers=headers, files=files)

    # if response.status_code == 200:
    #     print("Upload bem-sucedido!")
    #     print(response.json())
    # else:
    #     print(f"Erro {response.status_code}: {response.text}")
    return response







def get_veterinarian_info(email, token):
    """
    Busca as informações do veterinário na API.

    :param email: Email do veterinário
    :param token: Token de autenticação
    :return: Dicionário com as informações do veterinário ou None se houver erro
    """
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(f"{API_URL}/veterinarians/{email}", headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error("Veterinário não encontrado.")
        else:
            st.error("Erro ao buscar informações do veterinário.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão: {e}")
    return None

def register_user(name, email, password, crmv, phone=None):
    """
    Registra um novo usuário no sistema.

    :param name: Nome do usuário
    :param email: Email do usuário
    :param password: Senha do usuário
    :param crmv: CRMV do veterinário
    :param phone: Telefone opcional
    """
    response = requests.post(f"{API_URL}/veterinarian", json={
        "name": name,
        "email": email,
        "password": password,
        "crmv": crmv,
        "phone": phone
    })
    if response.status_code == 200:
        st.success("Cadastro realizado com sucesso! Faça login para acessar.")
    else:
        st.error("Erro ao cadastrar: " +
                 response.json().get("detail", "Erro desconhecido"))
        
def get_logo(email, token):
    """
    Faz o download do logo do veterinário a partir da API.

    :param email: Email do veterinário
    :param token: Token de autenticação
    :return: Caminho do arquivo da imagem baixada ou None em caso de erro
    """
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(f"{API_URL}/veterinarian/{email}/get-logo", headers=headers, stream=True)
        if response.status_code == 200:
            logo_path = f"{DOWNLOAD_DIR}/logo_{email}.png"
            with open(logo_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return logo_path
        elif response.status_code == 404:
            st.error("Logo não encontrado.")
        else:
            st.error("Erro ao buscar o logo.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão: {e}")
    return None

def get_signature(email, token):
    """
    """
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(f"{API_URL}/veterinarian/{email}/get-signature", headers=headers, stream=True)
        if response.status_code == 200:
            signature_path = f"{DOWNLOAD_DIR}/signature_{email}.png"
            with open(signature_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return signature_path
        elif response.status_code == 404:
            st.error("Signature não encontrado.")
        else:
            st.error("Erro ao buscar o signature.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de conexão: {e}")
    return None