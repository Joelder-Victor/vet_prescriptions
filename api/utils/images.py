import os
import requests
from dotenv import load_dotenv
import boto3
from botocore.client import Config

# Carregar variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")
PROJECT_REGION = os.getenv("PROJECT_REGION")
ACCESS_KEY = os.getenv("SUPABASE_KEY")
SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")
# Criação do cliente S3 usando boto3
s3_client = boto3.client(
    's3',
    region_name=PROJECT_REGION,
    endpoint_url=f"{SUPABASE_URL}",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(s3={'addressing_style': 'path'})
)


def download_image_from_supabase(object_key, download_path,object_key_path):
    #object_key_path = "logos/"+object_key
    
    try:
        response = s3_client.download_file(
            SUPABASE_BUCKET, object_key_path, f"{download_path}/{object_key}")
       
        return response

    except Exception as e:
        return f"Erro ao baixar o arquivo: {e}"


def upload_image_to_supabase(file_path, object_key):
    try:
        response = s3_client.upload_file(
            file_path, SUPABASE_BUCKET, object_key)
        print(f"Arquivo '{
              file_path}' enviado com sucesso para o Supabase em {response}.")
    except s3_client.exceptions.NoSuchBucket:
        print(f"Erro: O bucket '{
              SUPABASE_BUCKET}' não foi encontrado. Verifique se ele existe no Supabase.")
    except Exception as e:
        print(f"Erro ao enviar o arquivo: {str(e)}")
