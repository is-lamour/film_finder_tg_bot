from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("Найти фильм по названию"),
        KeyboardButton("Найти фильм по рейтингу"),
        KeyboardButton("Низкобюджетные фильмы"),
        KeyboardButton("Высокобюджетные фильмы"),
        KeyboardButton("История запросов")
    )
    return markup
