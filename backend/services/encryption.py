import os
from cryptography.fernet import Fernet
from config import VIP_ENCRYPTION_KEY

# Умная инициализация ключа (как было в твоем оригинальном боте)
try:
    if not VIP_ENCRYPTION_KEY or len(VIP_ENCRYPTION_KEY) < 40:
        raise ValueError("Неверный или пустой ключ")
    vip_fernet = Fernet(VIP_ENCRYPTION_KEY.encode('utf-8'))
except ValueError:
    print("⚠️ Неверный VIP_ENCRYPTION_KEY в .env. Генерируем новый...")

    # Генерируем правильный ключ
    new_key = Fernet.generate_key().decode('utf-8')

    # Находим путь к файлу .env и дописываем туда ключ
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    with open(env_path, 'a', encoding='utf-8') as f:
        f.write(f"\nVIP_ENCRYPTION_KEY={new_key}\n")

    vip_fernet = Fernet(new_key.encode('utf-8'))
    print("✅ Новый ключ успешно сгенерирован и автоматически сохранен в .env!")


def encrypt_vip_data(data) -> str:
    if data is None or data == "": return data
    return vip_fernet.encrypt(str(data).encode('utf-8')).decode('utf-8')


def decrypt_vip_data(data: str) -> str:
    if data is None or data == "": return data
    try:
        return vip_fernet.decrypt(str(data).encode('utf-8')).decode('utf-8')
    except Exception:
        return str(data)