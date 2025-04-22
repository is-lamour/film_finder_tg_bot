from datetime import datetime

search_history = {}


def save_to_history(message, film_data):
    chat_id = message.chat.id
    if chat_id not in search_history:
        search_history[chat_id] = []

    search_history[chat_id].append({
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'name': film_data['name'],
        'description': film_data['description'],
        'rating': film_data['rating']['kp'],
        'year': film_data['year'],
        'genres': [genre['name'] for genre in film_data['genres']],
        'age_rating': film_data['ageRating'],
        'poster': film_data['poster']['previewUrl'],
        'link': f'https://www.kinopoisk.ru/film/{film_data["id"]}'
    })


def print_film_info(data):
    genre_names = [genre['name'] for genre in data['genres']]
    age_rating = f"{data['ageRating']}+" if data['ageRating'] is not None else ""
    poster_url = data['poster']['previewUrl'] if data['poster']['previewUrl'] is not None else ""
    film_link = f"https://www.kinopoisk.ru/film/{data['id']}"

    return (f'\n*Название*: {data["name"] if data["name"] is not None else data["names"][0]["name"]}'
            f'\n*Год:* {data["year"]}'
            f'\n*Жанры:* {", ".join(genre_names)}'
            f'\n*Описание:* {data["description"]}'
            f'\n*Рейтинг:* КиноПоиск: {round(data["rating"]["kp"], 1)},\tIMDb: {data["rating"]["imdb"]}'
            f'\n*Возрастной рейтинг:* {age_rating}'
            f'\n*Постер*: {poster_url}'
            f'\n*Ссылка:* {film_link}')


def print_history_record(record):
    film_link = f"https://www.kinopoisk.ru/film/{record['id']}"
    return (f"\nДата поиска: {record['date']}"
            f"\nНазвание: {record['name']}"
            f"\nГод: {record['year']}"
            f"\nЖанры: {record['genres']}"
            f"\nОписание: {record['description']}"
            f"\nРейтинг: {record['rating']}"
            f"\nВозрастной рейтинг: {record['age_rating']}+"
            f"\nПостер: {record['poster']}"
            f'\nСсылка: {film_link}')