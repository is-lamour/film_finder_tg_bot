from telebot.handler_backends import State, StatesGroup

class SearchStates(StatesGroup):
    waiting_for_movie_title = State()
    waiting_for_movie_rating = State()