import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    API_SECRET_KEY = os.getenv("API_SECRET_KEY")
    API_KEY = os.getenv("API_KEY")
    

config = Config()
