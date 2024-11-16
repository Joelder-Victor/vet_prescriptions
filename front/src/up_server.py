import os
import requests
from dotenv import load_dotenv

load_dotenv()


API_URL = os.getenv("API_URL")

def wakeup_api():
  
 
    response = requests.get(f"{API_URL}")
    return response.status_code
       
    