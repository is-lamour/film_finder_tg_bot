import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

if not BOT_TOKEN or not RAPID_API_KEY:
    raise ValueError("BOT_TOKEN or RAPID_API_KEY is not set in .env file")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("movie_search", "Найти фильм по названию"),
    ("movie_by_rating", "Найти фильм по рейтингу"),
    ("low_budget_movie", "Низкобюджетные фильмы"),
    ("high_budget_movie", "Высокобюджетные фильмы"),
    ("history", "История запросов")
)
