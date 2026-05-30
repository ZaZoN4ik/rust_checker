import re
import html
from telebot import TeleBot
from telebot.types import Message
from states import user_states
from database.db import get_user_points, deduct_point
from api.steam import resolve_vanity_url
from services.profile import check_steam_profile
from api.battlemetrics import search_bm_players_by_name, get_bm_player_servers


def register_search_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda msg: msg.text == "🔍 Стим")
    def ask_steam_id(message: Message):
        chat_id = message.chat.id
        if get_user_points(chat_id) <= 0:
            bot.send_message(chat_id,
                             "У вас закончились баллы, купите VIP подписку или подождите до следующего дня (00:00) чтоб обновились баллы.")
            return
        user_states[chat_id] = "waiting_for_steam_id"
        bot.send_message(chat_id, "Введите Steam ID или ссылку на профиль Steam для поиска")

    @bot.message_handler(func=lambda msg: msg.text == "🔍 Ник")
    def ask_nickname(message: Message):
        chat_id = message.chat.id
        user_states[chat_id] = "waiting_for_rust_nickname"
        msg_text = (
            "Введите Ник игрока для поиска\n\n"
            "Обратите внимание, ник должен в точности соответствовать нику игрока, "
            "иначе бот его не найдет. А так же бот ищет игроков, которые были в онлайне "
            "за последние две недели."
        )
        bot.send_message(chat_id, msg_text)

    # Ловец текстового ввода (когда бот ждет Steam ID или Ник)
    @bot.message_handler(
        func=lambda msg: user_states.get(msg.chat.id) in ["waiting_for_steam_id", "waiting_for_rust_nickname"])
    def process_search_input(message: Message):
        chat_id = message.chat.id
        text = message.text
        current_state = user_states.get(chat_id)

        if current_state == "waiting_for_steam_id":
            if not deduct_point(chat_id):
                bot.send_message(chat_id,
                                 "У вас закончились баллы, купите VIP подписку или подождите до следующего дня.")
                user_states[chat_id] = None
                return

            extracted_steam_id = None
            match_id = re.search(r'7656119\d{10}', text)
            if match_id:
                extracted_steam_id = match_id.group(0)
            else:
                match_vanity = re.search(r'steamcommunity\.com/id/([^/\?\s]+)', text)
                if match_vanity:
                    vanity_name = match_vanity.group(1)
                    bot.send_message(chat_id,
                                     f"🔍 Преобразую ссылку <code>{html.escape(vanity_name)}</code> в SteamID...",
                                     parse_mode="HTML")
                    extracted_steam_id = resolve_vanity_url(vanity_name)
                elif " " not in text.strip() and "http" not in text:
                    bot.send_message(chat_id, f"🔍 Проверяю кастомную ссылку...", parse_mode="HTML")
                    extracted_steam_id = resolve_vanity_url(text.strip())

            if extracted_steam_id:
                bot.send_message(chat_id, f"⏳ Ищу профиль <code>{html.escape(extracted_steam_id)}</code>...",
                                 parse_mode="HTML")
                response_text, inline_markup = check_steam_profile(extracted_steam_id, chat_id)
                bot.send_message(chat_id, response_text, reply_markup=inline_markup, parse_mode="HTML",
                                 disable_web_page_preview=False)
                user_states[chat_id] = f"profile_{extracted_steam_id}"
            else:
                bot.send_message(chat_id,
                                 "❌ Не удалось найти профиль. Отправь прямую ссылку на профиль, кастомную ссылку или 17 цифр SteamID.")

        elif current_state == "waiting_for_rust_nickname":
            nickname = text.strip()
            bot.send_message(chat_id, f"⏳ Ищу игрока с ником <code>{html.escape(nickname)}</code>", parse_mode="HTML")

            player_ids = search_bm_players_by_name(nickname)
            if not player_ids:
                bot.send_message(chat_id,
                                 f"❌ Игрок с ником <code>{html.escape(nickname)}</code> не найден в Battlemetrics.",
                                 parse_mode="HTML")
            else:
                servers = []
                for pid in player_ids:
                    servers = get_bm_player_servers(pid)
                    if servers: break

                if not servers:
                    bot.send_message(chat_id,
                                     "❌ Игрок найден, либо данный игрок не заходил в раст в течении 2-х последних недель.")
                else:
                    msg = f"🔍 <b>Последние серверы Rust для {html.escape(nickname)}:</b>\n\n"
                    for s in servers:
                        name = html.escape(s.get("name", "Неизвестный сервер"))
                        ip, port = s.get("ip", ""), s.get("port", "")
                        status = "🟢" if s.get("status") == "online" else "🔴"
                        msg += f"{status} <b>{name}</b>\nconnect {ip}:{port}\n\n"
                    bot.send_message(chat_id, msg, parse_mode="HTML")

            user_states[chat_id] = None