from telebot import TeleBot
from database.db import remove_tracked_user, deduct_point
from services.profile import check_steam_profile


def register_tracking_handlers(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("untrack_"))
    def handle_untrack(call):
        steam_id = call.data.split("_")[1]
        chat_id = call.message.chat.id
        remove_tracked_user(chat_id, steam_id)

        bot.answer_callback_query(call.id, "❌ Отслеживание отменено.")
        try:
            bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        except Exception:
            pass

    @bot.callback_query_handler(func=lambda call: call.data.startswith("details_"))
    def handle_details(call):
        steam_id = call.data.split("_")[1]
        chat_id = call.message.chat.id

        if not deduct_point(chat_id):
            bot.answer_callback_query(call.id, "❌ У вас закончились баллы!")
            bot.send_message(chat_id, "У вас закончились баллы, купите VIP подписку или подождите до 00:00.")
            return

        bot.answer_callback_query(call.id, "⏳ Загружаю данные...")
        response_text, inline_markup = check_steam_profile(steam_id, chat_id)
        bot.send_message(chat_id, response_text, reply_markup=inline_markup, parse_mode="HTML",
                         disable_web_page_preview=False)