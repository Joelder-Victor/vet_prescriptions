import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

def authenticate_user(email, password):
    """
    Faz a autenticação do usuário e retorna o token de acesso.

    :param email: Email do usuário
    :param password: Senha do usuário
    :return: Token de acesso ou None se a autenticação falhar
    """
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'password',
        'username': email,
        'password': password,
        'scope': '',
        'client_id': 'string',
        'client_secret': 'string'
    }
    response = requests.post(f"{API_URL}/login", headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        st.error("Email ou senha incorretos.")
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
