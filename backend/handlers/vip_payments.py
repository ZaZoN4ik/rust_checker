from telebot import TeleBot, types
from database.db import add_vip
from states import user_states


def register_vip_handlers(bot: TeleBot):
    # 1. Отправка счета (Invoice) при выборе тарифа
    @bot.message_handler(func=lambda msg: msg.text in ["👑 VIP подписка на месяц", "💎 VIP подписка на неделю"])
    def handle_vip_purchase(message):
        chat_id = message.chat.id
        text = message.text

        if text == "👑 VIP подписка на месяц":
            bot.send_invoice(
                chat_id,
                title="VIP на месяц",
                description="Оплата VIP подписки на 30 дней. Безлимитные запросы и авто-уведомления.",
                invoice_payload="vip_month",
                provider_token="",  # Для Telegram Stars токен провайдера должен быть ПУСТЫМ
                currency="XTR",
                prices=[types.LabeledPrice(label="VIP на месяц", amount=100)]  # 100 звезд
            )
        elif text == "💎 VIP подписка на неделю":
            bot.send_invoice(
                chat_id,
                title="VIP на неделю",
                description="Оплата VIP подписки на 7 дней. Безлимитные запросы и авто-уведомления.",
                invoice_payload="vip_week",
                provider_token="",
                currency="XTR",
                prices=[types.LabeledPrice(label="VIP на неделю", amount=50)]  # 50 звезд
            )

    # 2. Подтверждение перед списанием (Pre-checkout)
    # Telegram спрашивает бота, готов ли он предоставить услугу, прежде чем снять звезды
    @bot.pre_checkout_query_handler(func=lambda query: True)
    def process_pre_checkout_query(pre_checkout_query):
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    # 3. Обработка успешной оплаты
    @bot.message_handler(content_types=['successful_payment'])
    def process_successful_payment(message):
        chat_id = message.chat.id
        payment_info = message.successful_payment
        payload = payment_info.invoice_payload

        # Определяем количество дней в зависимости от того, что купил юзер
        days = 30 if payload == "vip_month" else 7

        # Выдаем VIP в базу данных
        add_vip(chat_id, days)

        bot.send_message(
            chat_id,
            f"🎉 <b>Спасибо за покупку!</b>\n\n"
            f"Оплачено: {payment_info.total_amount} XTR ⭐️\n"
            f"Вам выдана VIP подписка на <b>{days} дней</b>!\n"
            f"Теперь у вас 1000 баллов ежедневно.",
            parse_mode="HTML"
        )

        # Сбрасываем состояние юзера
        user_states[chat_id] = None