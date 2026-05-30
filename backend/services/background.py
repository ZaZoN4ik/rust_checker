import time
import requests
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import STEAM_API_KEY
from database.db import get_tracked_users, get_users_tracking, deduct_point
from services.profile import check_steam_profile
from states import player_states

def background_monitor(bot: TeleBot):
    print("Фоновый мониторинг запущен...")
    while True:
        try:
            time.sleep(30)
            all_tracked_steam_ids = get_tracked_users()
            if not all_tracked_steam_ids:
                continue

            players_data = {}
            # Разбиваем на чанки по 100, как требует Steam API
            for i in range(0, len(all_tracked_steam_ids), 100):
                chunk = all_tracked_steam_ids[i:i+100]
                chunk_str = ",".join(chunk)
                url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={chunk_str}"
                try:
                    response = requests.get(url, timeout=10).json()
                    for p in response.get('response', {}).get('players', []):
                        players_data[p.get('steamid')] = p
                except Exception as e:
                    print(f"Ошибка запроса Steam API: {e}")

            # Проверяем изменения статусов
            for steam_id in all_tracked_steam_ids:
                player = players_data.get(steam_id)
                if not player: continue

                is_online = player.get('personastate', 0) != 0
                current_state = {
                    'is_online': is_online,
                    'gameextrainfo': player.get('gameextrainfo', ''),
                    'gameserverip': player.get('gameserverip', '')
                }

                if steam_id in player_states:
                    if player_states[steam_id] != current_state:
                        users_tracking = get_users_tracking(steam_id)
                        for chat_id in users_tracking:
                            if not deduct_point(chat_id): continue

                            response_text, _ = check_steam_profile(steam_id, chat_id)
                            inline_kb = InlineKeyboardMarkup()
                            inline_kb.row(InlineKeyboardButton("🚫 Отменить отслеживание", callback_data=f"untrack_{steam_id}"))
                            inline_kb.row(InlineKeyboardButton("🔄️ Обновить", callback_data=f"details_{steam_id}"))

                            try:
                                bot.send_message(
                                    chat_id,
                                    f"🔔 <b>Обновление статуса:</b>\n\n{response_text}",
                                    reply_markup=inline_kb,
                                    parse_mode="HTML",
                                    disable_web_page_preview=False
                                )
                            except Exception as e:
                                print(f"Ошибка отправки уведомления {chat_id}: {e}")
                            time.sleep(0.05) # Защита от лимитов Telegram

                player_states[steam_id] = current_state

        except Exception as e:
            print(f"Критическая ошибка в background_monitor: {e}")
            time.sleep(30)