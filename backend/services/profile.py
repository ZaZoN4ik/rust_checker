import requests
import html
from datetime import datetime
from config import STEAM_API_KEY
from api.steam import get_rust_hours
from keyboards.reply import get_profile_reply_menu

def check_steam_profile(steam_id, chat_id):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}"
    try:
        response = requests.get(url, timeout=10).json()
        players = response.get('response', {}).get('players', [])
        if not players:
            return "❌ Игрок не найден.", None

        player = players[0]
        name = player.get('personaname', 'Неизвестно')
        safe_name = html.escape(name)
        profile_url = player.get('profileurl', '')

        time_created = player.get('timecreated')
        creation_date = datetime.fromtimestamp(time_created).strftime('%d.%m.%Y') if time_created else "Скрыто настройками"

        persona_state = player.get('personastate', 0)
        game_name = player.get('gameextrainfo')

        # Статус
        status_text = "⚫️ Не в сети ⚫️"
        if persona_state == 1: status_text = "🟢 В сети 🟢"
        elif persona_state == 3: status_text = "🟡 Нет на месте 🟡"
        elif persona_state == 4: status_text = "💤 Спит 💤"

        game_line = "\n🎮 Игра: не в игре"
        server_line = ""
        if game_name:
            game_line = f"\n🎮 Игра: {game_name}"
            gameserverip = player.get('gameserverip')
            if gameserverip and game_name == "Rust":
                server_line = f"\n🌐 Сервер: connect {gameserverip}"

        hours = get_rust_hours(steam_id)

        text = (
            f"👤 Имя: {safe_name}\n"
            f"🆔 Steam_id: <code>{steam_id}</code>\n"
            f"💬 Статус: {status_text}{game_line}{server_line}\n"
            f"📅 Аккаунт создан: {creation_date}\n"
            f"⏰ Часов в игре: {hours}\n\n"
            f"<a href='{profile_url}'>Steamcommunity :: {safe_name}</a>"
        )
        return text, get_profile_reply_menu(steam_id, chat_id)

    except Exception as e:
        print(f"Error in check_steam_profile: {e}")
        return "⚠ Произошла ошибка сервера.", None