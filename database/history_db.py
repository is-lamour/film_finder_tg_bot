from datetime import datetime
import sqlite3
import logging
import json

logging.basicConfig(level=logging.INFO)


def get_db_connection():
    conn = sqlite3.connect('search_history.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS search_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  date TEXT,
                  name TEXT,
                  description TEXT,
                  rating REAL,
                  year INTEGER,
                  genres TEXT,
                  age_rating INTEGER,
                  poster TEXT,
                  link TEXT)''')
    conn.commit()
    conn.close()


def save_to_history(user_id, movie_data):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        # Генерируем строку с жанрами
        genres = ', '.join([genre['name'] for genre in movie_data['genres']])
        # Сохраняем запись в базу данных
        c.execute('''INSERT INTO search_history 
                     (user_id, date, name, description, rating, year, genres, age_rating, poster, link)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (user_id,
                   datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   movie_data['name'],
                   movie_data['description'],
                   movie_data['rating']['kp'],
                   movie_data['year'],
                   genres,
                   movie_data['ageRating'],
                   movie_data['poster']['previewUrl'],
                   f"https://www.kinopoisk.ru/film/{movie_data['id']}"))
        conn.commit()
        logging.info(f"Saved movie to history for user {user_id}: {movie_data['name']}")
    except Exception as e:
        logging.error(f"Error saving to history: {e}")
    finally:
        conn.close()


def get_search_history(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        # Выполняем запрос для получения истории
        c.execute('SELECT * FROM search_history WHERE user_id = ? ORDER BY date DESC', (user_id,))
        history = c.fetchall()
        logging.info(f"Retrieved {len(history)} records from history for user {user_id}")
        return history
    except Exception as e:
        logging.error(f"Error getting search history: {e}")
        return []
    finally:
        conn.close()


def print_history_record(record):
    rating_kp = round(record['rating'], 1) if isinstance(record['rating'], (int, float)) else "N/A"
    age_rating = f"{record['age_rating']}+" if record['age_rating'] is not None else ""
    poster_url = record['poster'] if record['poster'] is not None else ""

    return (f"\n*Дата поиска*: {record['date']}"
            f"\n*Название*: {record['name']}"
            f"\n*Год*: {record['year']}"
            f"\n*Жанры*: {record['genres']}"
            f"\n*Описание*: {record['description']}"
            f"\n*Рейтинг*: КиноПоиск: {rating_kp}"
            f"\n*Возрастной рейтинг:* {age_rating}"
            f"\n*Постер*: {poster_url}"
            f"\n*Ссылка:* https://www.kinopoisk.ru/film/{record['id']}")