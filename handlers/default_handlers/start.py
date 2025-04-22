from telebot.types import Message
from keyboards.reply.main_menu import main_menu_keyboard
from loader import bot

@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.reply_to(
        message,
        f"Добро пожаловать, {message.from_user.full_name}! Я бот, созданный чтобы искать фильмы.",
        reply_markup=main_menu_keyboard()
    )