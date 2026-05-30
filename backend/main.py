import threading
import telebot
from config import TELEGRAM_TOKEN
from database.db import init_db
from services.background import background_monitor

# Импорты регистраторов хэндлеров
from handlers.basic import register_basic_handlers
from handlers.search import register_search_handlers
from handlers.webapp import register_webapp_handlers
from handlers.tracking import register_tracking_handlers
from handlers.vip_payments import register_vip_handlers

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def main():
    print("Инициализация базы данных MySQL...")
    init_db()

    print("Регистрация обработчиков...")
    register_basic_handlers(bot)
    register_search_handlers(bot)
    register_webapp_handlers(bot)
    register_tracking_handlers(bot)
    register_vip_handlers(bot)

    print("Запуск фонового мониторинга...")
    monitor_thread = threading.Thread(target=background_monitor, args=(bot,), daemon=True)
    monitor_thread.start()

    print("Бот успешно запущен!")
    bot.infinity_polling()

if __name__ == "__main__":
    main()