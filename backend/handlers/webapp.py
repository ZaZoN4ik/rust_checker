import json
import html
import re
import requests
from telebot import TeleBot, types
from telebot.types import Message
from states import user_states
from api.battlemetrics import search_bm_players_by_name, get_bm_player_servers
from api.steam import resolve_vanity_url
from services.profile import check_steam_profile
from database.db import get_tracked_users, deduct_point
from config import STEAM_API_KEY


def register_webapp_handlers(bot: TeleBot):
    @bot.message_handler(content_types=['web_app_data'])
    def handle_web_app_data(message: Message):
        chat_id = message.chat.id
        raw_data = message.web_app_data.data

        try:
            data = json.loads(raw_data)
            action = data.get('action')

            # --- 1. ПОИСК ПО НИКУ ---
            if action == 'SEARCH_NICK':
                nickname = data.get('nickname')
                bot.send_message(chat_id,
                                 f"📱 <b>Запрос из приложения:</b>\n⏳ Ищу игрока <code>{html.escape(nickname)}</code>",
                                 parse_mode="HTML")

                player_ids = search_bm_players_by_name(nickname)
                if not player_ids:
                    bot.send_message(chat_id,
                                     f"❌ Игрок <code>{html.escape(nickname)}</code> не найден в Battlemetrics.",
                                     parse_mode="HTML")
                    return

                servers = []
                for pid in player_ids:
                    servers = get_bm_player_servers(pid)
                    if servers: break

                if not servers:
                    bot.send_message(chat_id, "❌ Игрок не заходил в Rust в течение 2-х последних недель.")
                else:
                    msg = f"🔍 <b>Последние серверы Rust для {html.escape(nickname)}:</b>\n\n"
                    for s in servers:
                        name = html.escape(s.get("name", "Неизвестный сервер"))
                        ip, port = s.get("ip", ""), s.get("port", "")
                        status = "🟢" if s.get("status") == "online" else "🔴"
                        msg += f"{status} <b>{name}</b>\nconnect {ip}:{port}\n\n"
                    bot.send_message(chat_id, msg, parse_mode="HTML")

            # --- 2. ПОИСК ПО STEAM ID ---
            elif action == 'SEARCH_STEAM':
                text = data.get('steamId')
                if not deduct_point(chat_id):
                    bot.send_message(chat_id, "❌ У вас закончились баллы, купите VIP подписку или подождите до 00:00.")
                    return

                bot.send_message(chat_id,
                                 f"📱 <b>Запрос из приложения:</b>\n⏳ Обрабатываю <code>{html.escape(text)}</code>",
                                 parse_mode="HTML")

                extracted_steam_id = None
                match_id = re.search(r'7656119\d{10}', text)

                if match_id:
                    extracted_steam_id = match_id.group(0)
                else:
                    match_vanity = re.search(r'steamcommunity\.com/id/([^/\?\s]+)', text)
                    if match_vanity:
                        vanity_name = match_vanity.group(1)
                        extracted_steam_id = resolve_vanity_url(vanity_name)
                    elif " " not in text.strip() and "http" not in text:
                        extracted_steam_id = resolve_vanity_url(text.strip())

                if extracted_steam_id:
                    response_text, inline_markup = check_steam_profile(extracted_steam_id, chat_id)
                    bot.send_message(chat_id, response_text, reply_markup=inline_markup, parse_mode="HTML",
                                     disable_web_page_preview=False)
                    user_states[chat_id] = f"profile_{extracted_steam_id}"
                else:
                    bot.send_message(chat_id, "❌ Не удалось найти профиль. Убедитесь, что ссылка или ID верны.")

            # --- 3. ПОЛУЧИТЬ ОТСЛЕЖИВАНИЯ ---
            elif action == 'GET_TRACKINGS':
                tracked = get_tracked_users(chat_id)
                if not tracked:
                    bot.send_message(chat_id, "📱 Ваши отслеживания пусты.")
                    return

                bot.send_message(chat_id, "⏳ Собираю актуальные данные...")

                # Получаем имена игроков из Steam
                chunk_str = ",".join(tracked)
                url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={chunk_str}"
                name_map = {}
                try:
                    response = requests.get(url, timeout=10).json()
                    players = response.get('response', {}).get('players', [])
                    name_map = {p.get('steamid'): p.get('personaname', 'Неизвестно') for p in players}
                except Exception:
                    pass

                # Создаем Inline-клавиатуру для каждого игрока
                markup = types.InlineKeyboardMarkup()
                for steam_id in tracked:
                    name = name_map.get(steam_id, steam_id)
                    markup.row(types.InlineKeyboardButton(f"👤 {name}", callback_data=f"details_{steam_id}"))

                bot.send_message(
                    chat_id,
                    "📡 <b>Ваши отслеживания:</b>\nНажмите на игрока, чтобы посмотреть информацию или удалить его.",
                    reply_markup=markup,
                    parse_mode="HTML"
                )

        except json.JSONDecodeError:
            bot.send_message(chat_id, "❌ Ошибка при обработке данных Web App.")