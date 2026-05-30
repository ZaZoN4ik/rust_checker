import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8876780305:AAEkX6Vtv0Uk1zgms6VCfJll5gBg57topLY")
STEAM_API_KEY = os.environ.get("STEAM_API_KEY", "53B98FD77D5C5D8AE35FF8B42CB3E0C4")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")
VIP_ENCRYPTION_KEY = os.environ.get("VIP_ENCRYPTION_KEY", "")

# Настройки MySQL
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'admin',
    'database': 'rust',
    'autocommit': True
}