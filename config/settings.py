import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY_GEMINI")
TOKEN = os.getenv("TG_TOKEN")