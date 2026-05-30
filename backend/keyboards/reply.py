from telebot import types
from config import WEBAPP_URL


def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    if WEBAPP_URL and WEBAPP_URL.startswith("https://") and "localhost" not in WEBAPP_URL:
        web_app = types.WebAppInfo(WEBAPP_URL)
        markup.row(types.KeyboardButton("🚀 Открыть меню", web_app=web_app))

    markup.add(types.KeyboardButton("🔍 Стим"), types.KeyboardButton("🔍 Ник"))
    markup.add(types.KeyboardButton("👁 Мои отслеживания"),
               types.KeyboardButton("❓ Ответы на вопросы"))
    markup.add(types.KeyboardButton("🧱 Калькулятор рейда"),
               types.KeyboardButton("👤 Мой профиль"))
    markup.row(types.KeyboardButton("👑 VIP подписка"))
    return markup


def get_faq_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("❓ Часто задаваемые вопросы"))
    markup.row(types.KeyboardButton("🔎 Как найти steam id"), types.KeyboardButton("🪙 Что такое баллы?"))
    markup.row(types.KeyboardButton("📞 Связаться с администратором"))
    markup.row(types.KeyboardButton("🔙 Назад в меню"))
    return markup


def get_vip_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("👑 VIP подписка на месяц"))
    markup.add(types.KeyboardButton("💎 VIP подписка на неделю"))
    markup.add(types.KeyboardButton("🔙 Назад в меню"))
    return markup


def get_back_to_faq_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("🔙 Назад"))
    return markup


def get_my_profile_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("🔙 Назад в меню"))
    return markup


def get_profile_reply_menu(steam_id, chat_id):
    from database.db import get_tracked_users
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    user_tracked_list = get_tracked_users(chat_id)

    if steam_id in user_tracked_list:
        track_btn = types.KeyboardButton("🚫 Отменить отслеживание")
    else:
        track_btn = types.KeyboardButton("👁 Отслеживать")

    markup.row(types.KeyboardButton("👥 Друзья (Rust)"), track_btn)
    markup.row(types.KeyboardButton("🔄 Обновить"))
    markup.row(types.KeyboardButton("🔙 Назад в меню"))
    return markup