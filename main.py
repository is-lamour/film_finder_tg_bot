from loader import bot
import handlers  # Это импортирует весь пакет handlers
from database.history_db import init_db
import logging
import sys
import os
from threading import Thread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Явно импортируем обработчики start и help
from handlers.default_handlers.start import bot_start
from handlers.default_handlers.help import bot_help


def check_running_instances():
    """Проверяет, не запущен ли уже экземпляр бота"""
    try:
        if os.path.exists('bot.lock'):
            logger.error("Бот уже запущен. Если это не так, удалите файл 'bot.lock'")
            sys.exit(1)

        with open('bot.lock', 'w') as f:
            f.write(str(os.getpid()))

    except Exception as e:
        logger.error(f"Ошибка при проверке запущенных экземпляров: {e}")
        sys.exit(1)


def cleanup():
    """Очищает файл блокировки при завершении работы"""
    try:
        if os.path.exists('bot.lock'):
            os.remove('bot.lock')
    except Exception as e:
        logger.error(f"Ошибка при очистке файла блокировки: {e}")


if __name__ == "__main__":
    try:
        # Проверяем, не запущен ли уже бот
        check_running_instances()

        # Регистрируем очистку при завершении
        import atexit

        atexit.register(cleanup)

        # Инициализация базы данных
        init_db()

        # Явно регистрируем обработчики
        bot.register_message_handler(bot_start, commands=['start'])
        bot.register_message_handler(bot_help, commands=['help'])

        # Запуск бота
        logger.info("Бот запущен")
        bot.infinity_polling()

    except KeyboardInterrupt:
        logger.info("Бот остановлен")
        cleanup()
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        cleanup()
        sys.exit(1)
