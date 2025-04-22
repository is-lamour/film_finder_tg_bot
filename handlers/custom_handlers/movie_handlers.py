from telebot.types import Message
from loader import bot
from states.search_states import SearchStates
from utils.api_request import search_movie_by_title, search_movie_by_rating, search_low_budget_movies, search_high_budget_movies
from database.history_db import get_search_history, save_to_history
from utils.history_utils import print_film_info, print_history_record
from handlers.default_handlers.start import bot_start
from handlers.default_handlers.help import bot_help

import logging

logging.basicConfig(level=logging.INFO)

@bot.message_handler(func=lambda message: message.text == "Найти фильм по названию")
def movie_search_text(message: Message):
    movie_search(message)

@bot.message_handler(func=lambda message: message.text == "Найти фильм по рейтингу")
def movie_by_rating_text(message: Message):
    movie_by_rating(message)

@bot.message_handler(func=lambda message: message.text == "Низкобюджетные фильмы")
def low_budget_movie_text(message: Message):
    low_budget_movie(message)

@bot.message_handler(func=lambda message: message.text == "Высокобюджетные фильмы")
def high_budget_movie_text(message: Message):
    high_budget_movie(message)

@bot.message_handler(func=lambda message: message.text == "История запросов")
def show_history_text(message: Message):
    show_history(message)

@bot.message_handler(commands=["movie_search"])
def movie_search(message: Message):
    try:
        bot.set_state(message.from_user.id, SearchStates.waiting_for_movie_title, message.chat.id)
        bot.send_message(message.chat.id, 'Введите название фильма')
    except Exception as e:
        logging.error(f"Error setting state in movie_search: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка. Попробуйте позже.')

@bot.message_handler(state=SearchStates.waiting_for_movie_title)
def handle_movie_title(message: Message):
    try:
        movies = search_movie_by_title(message.text)
        if movies:
            for movie in movies:
                bot.send_message(message.chat.id, print_film_info(movie), parse_mode="Markdown")
                save_to_history(message.from_user.id, movie)  # movie передается правильно
        else:
            bot.send_message(message.chat.id, 'Ничего не найдено по вашему запросу.')
    except Exception as e:
        logging.error(f"Error in handle_movie_title: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка при поиске фильма. Попробуйте позже.')
    finally:
        bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(commands=["movie_by_rating"])
def movie_by_rating(message: Message):
    try:
        bot.set_state(message.from_user.id, SearchStates.waiting_for_movie_rating, message.chat.id)
        bot.send_message(message.chat.id, 'Введите рейтинг или диапазон через пробел (7 7.5):')
    except Exception as e:
        logging.error(f"Error setting state in movie_by_rating: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка. Попробуйте позже.')

@bot.message_handler(state=SearchStates.waiting_for_movie_rating)
def handle_movie_rating(message: Message):
    try:
        movies = search_movie_by_rating(message.text)
        if movies:
            for movie in movies:
                bot.send_message(message.chat.id, print_film_info(movie), parse_mode="Markdown")
                save_to_history(message.from_user.id, movie)
        else:
            bot.send_message(message.chat.id, 'Ничего не найдено по вашему запросу.')
    except Exception as e:
        logging.error(f"Error in handle_movie_rating: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка при поиске фильма. Попробуйте позже.')
    finally:
        bot.delete_state(message.from_user.id, message.chat.id)

@bot.message_handler(commands=["low_budget_movie"])
def low_budget_movie(message: Message):
    bot.send_message(message.chat.id, 'Поиск фильмов с низким бюджетом (до 1 000 000$).')
    movies = search_low_budget_movies()
    if movies:
        for movie in movies:
            bot.send_message(message.chat.id, print_film_info(movie), parse_mode="Markdown")
            save_to_history(message.from_user.id, movie)
    else:
        bot.send_message(message.chat.id, 'Ничего не найдено по вашему запросу.')

@bot.message_handler(commands=["high_budget_movie"])
def high_budget_movie(message: Message):
    bot.send_message(message.chat.id, 'Поиск фильмов с высоким бюджетом (более 100 000 000$).')
    movies = search_high_budget_movies()
    if movies:
        for movie in movies:
            bot.send_message(message.chat.id, print_film_info(movie), parse_mode="Markdown")
            save_to_history(message.from_user.id, movie)
    else:
        bot.send_message(message.chat.id, 'Ничего не найдено по вашему запросу.')

@bot.message_handler(commands=["history"])
def show_history(message: Message):
    try:
        history = get_search_history(message.from_user.id)
        if history:
            bot.send_message(message.chat.id, 'История запросов:')
            for record in history:
                bot.send_message(message.chat.id, print_history_record(record))
        else:
            bot.send_message(message.chat.id, 'История запросов пуста.')
    except Exception as e:
        logging.error(f"Error in show_history: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка при получении истории. Попробуйте позже.')

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_all_messages(message: Message):
    state = bot.get_state(message.from_user.id, message.chat.id)
    if state == SearchStates.waiting_for_movie_title.name:
        handle_movie_title(message)
    elif state == SearchStates.waiting_for_movie_rating.name:
        handle_movie_rating(message)
    elif message.text.lower() in ['/start', '/help']:
        # Пропускаем обработку этих команд, чтобы их могли обработать соответствующие обработчики
        return
    else:
        bot.send_message(message.chat.id, "Пожалуйста, используйте команды для взаимодействия с ботом.")

