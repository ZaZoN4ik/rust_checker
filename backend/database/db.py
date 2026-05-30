import mysql.connector
import time
from datetime import datetime, timezone, timedelta
from config import DB_CONFIG
from services.encryption import encrypt_vip_data, decrypt_vip_data


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracked_users (
                chat_id BIGINT,
                steam_id VARCHAR(255),
                PRIMARY KEY (chat_id, steam_id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vip_users (
                chat_id BIGINT PRIMARY KEY,
                vip_until VARCHAR(255)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_points (
                chat_id BIGINT PRIMARY KEY,
                points INT,
                last_reset_date VARCHAR(50)
            )
        ''')
        conn.close()
        print("База данных MySQL успешно инициализирована.")
    except Exception as e:
        print("Ошибка подключения к MySQL:", e)


def add_vip(chat_id, days):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT vip_until FROM vip_users WHERE chat_id = %s', (chat_id,))
    row = cursor.fetchone()

    current_time = int(time.time())
    if row and row[0]:
        try:
            current_expiration = int(decrypt_vip_data(row[0]))
            if current_expiration < current_time:
                current_expiration = current_time
        except Exception:
            current_expiration = current_time
    else:
        current_expiration = current_time

    new_expiration = current_expiration + (days * 24 * 60 * 60)
    cursor.execute('''
        REPLACE INTO vip_users (chat_id, vip_until)
        VALUES (%s, %s)
    ''', (chat_id, encrypt_vip_data(str(new_expiration))))

    tz = timezone(timedelta(hours=3))
    today_str = datetime.now(tz).strftime('%Y-%m-%d')
    cursor.execute('''
        REPLACE INTO user_points (chat_id, points, last_reset_date)
        VALUES (%s, %s, %s)
    ''', (chat_id, 1000, today_str))
    conn.close()


def get_vip_status(chat_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT vip_until FROM vip_users WHERE chat_id = %s', (chat_id,))
    row = cursor.fetchone()
    conn.close()

    if not row or not row[0]:
        return "🚫 Не активна", None

    try:
        expiration_ts = int(decrypt_vip_data(row[0]))
        current_time = int(time.time())
        if expiration_ts > current_time:
            exp_date = datetime.fromtimestamp(expiration_ts).strftime('%d.%m.%Y %H:%M')
            return "👑 Активна", exp_date
        else:
            return "🚫 Не активна", None
    except Exception:
        return "🚫 Не активна", None


def get_user_points(chat_id):
    vip_status, _ = get_vip_status(chat_id)
    max_points = 1000 if vip_status == "👑 Активна" else 20
    tz = timezone(timedelta(hours=3))
    today_str = datetime.now(tz).strftime('%Y-%m-%d')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT points, last_reset_date FROM user_points WHERE chat_id = %s', (chat_id,))
    row = cursor.fetchone()

    if not row or row[1] != today_str:
        cursor.execute('''
            REPLACE INTO user_points (chat_id, points, last_reset_date)
            VALUES (%s, %s, %s)
        ''', (chat_id, max_points, today_str))
        conn.close()
        return max_points
    conn.close()
    return row[0]


def deduct_point(chat_id):
    current = get_user_points(chat_id)
    if current <= 0: return False
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE user_points SET points = points - 1 WHERE chat_id = %s', (chat_id,))

    if current - 1 == 0:
        cursor.execute('DELETE FROM tracked_users WHERE chat_id = %s', (chat_id,))
        # Уведомление об очистке отслеживаний будет отправляться из хэндлера
    conn.close()
    return True


def get_tracked_users(chat_id=None):
    conn = get_db()
    cursor = conn.cursor()
    if chat_id:
        cursor.execute('SELECT steam_id FROM tracked_users WHERE chat_id = %s', (chat_id,))
    else:
        cursor.execute('SELECT DISTINCT steam_id FROM tracked_users')
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


def add_tracked_user(chat_id, steam_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM tracked_users WHERE chat_id = %s', (chat_id,))
    if cursor.fetchone()[0] >= 15:
        conn.close()
        return False
    cursor.execute('INSERT IGNORE INTO tracked_users (chat_id, steam_id) VALUES (%s, %s)', (chat_id, steam_id))
    conn.close()
    return True


def remove_tracked_user(chat_id, steam_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tracked_users WHERE chat_id = %s AND steam_id = %s', (chat_id, steam_id))
    conn.close()


def get_users_tracking(steam_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT chat_id FROM tracked_users WHERE steam_id = %s', (steam_id,))
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result