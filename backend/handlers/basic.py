from telebot import TeleBot
from telebot.types import Message
from states import user_states
from keyboards.reply import get_main_menu, get_faq_menu, get_vip_menu, get_my_profile_menu
from database.db import get_vip_status, get_user_points
from datetime import datetime, timezone, timedelta


def register_basic_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        user_states[message.chat.id] = None
        bot.send_message(message.chat.id, "Привет! Выбери нужное действие:", reply_markup=get_main_menu())

    @bot.message_handler(func=lambda msg: msg.text in ["🔙 Назад в меню", "🔙 Назад"])
    def back_to_menu(message: Message):
        send_welcome(message)

    @bot.message_handler(func=lambda msg: msg.text == "👑 VIP подписка")
    def vip_menu(message: Message):
        user_states[message.chat.id] = "vip_menu"
        bot.send_message(message.chat.id, "Выберите вариант:", reply_markup=get_vip_menu())

    @bot.message_handler(func=lambda msg: msg.text == "❓ Ответы на вопросы")
    def handle_faq(message: Message):
        user_states[message.chat.id] = "faq"
        bot.send_message(message.chat.id, "Часто задаваемые вопросы:", reply_markup=get_faq_menu())

    @bot.message_handler(func=lambda msg: msg.text == "👤 Мой профиль")
    def handle_profile(message: Message):
        user_id = message.from_user.id
        vip_status, vip_until_str = get_vip_status(user_id)
        current_points = get_user_points(user_id)

        tz = timezone(timedelta(hours=3))
        now = datetime.now(tz)
        tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        hours, remainder = divmod(int((tomorrow - now).total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)

        profile_text = (
            f"id : {user_id}\n\n"
            f"Баллы: {current_points}\n"
            f"До обновления баллов осталось {hours}ч {minutes}м\n\n"
            f"Подписка : {vip_status}\n"
            f"Окончание: {vip_until_str if vip_until_str else '🚫 Не активна'}"
        )
        user_states[user_id] = "my_profile"
        bot.send_message(message.chat.id, profile_text, reply_markup=get_my_profile_menu())