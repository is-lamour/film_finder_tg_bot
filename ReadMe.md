# Телеграм-бот для поиска фильмов

# 🎬 Film Finder Bot - Telegram-бот для поиска фильмов

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)](https://core.telegram.org/bots/api)

Бот для поиска фильмов через API Кинопоиска с историей запросов.

## ✨ Функционал

- 🔍 Поиск по названию
- ⭐ Фильтрация по рейтингу (КиноПоиск/IMDb)
- 💰 Низкобюджетные фильмы (<$1M)
- 🚀 Высокобюджетные фильмы (>$100M)
- 📚 История поиска
- 🎛️ Интерактивное меню

## 🛠 Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/ваш-ник/film-finder-bot.git && cd film-finder-bot
```

2. Установите зависимости:

```
pip install -r requirements.txt
```

3. Создайте `.env` файл:

```
BOT_TOKEN="ваш_токен_от_BotFather"
RAPID_API_KEY="ваш_ключ_с_kinopoisk.dev"
```

4. Запустите:

```
python main.py
```

## 🖥 Команды


| Кнопка/Команда        | Действие                       |
| ---------------------------------- | -------------------------------------- |
| `/start`                           | Главное меню                |
| "Найти по названию" | Поиск фильма                |
| "Фильмы 7+ рейтинг"   | Подборка по рейтингу |
| `/history`                         | Показать историю        |

## 🐳 Docker

```
docker-compose up --build
```


Этот бот предоставляет информацию о фильмах, используя API Кинопоиска.

## Функционал

1. Поиск фильма по названию
2. Поиск фильма по рейтингу
3. Поиск низкобюджетных фильмов
4. Поиск высокобюджетных фильмов
5. Просмотр истории поиска

## Установка и настройка

1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`
3. Создайте файл `.env` в корневой директории проекта
4. Добавьте в `.env` следующие переменные:

   ```
   BOT_TOKEN=your_telegram_bot_token
   RAPID_API_KEY=your_kinopoisk_api_key
   ```

   - `BOT_TOKEN`: Получите токен у [@BotFather](https://t.me/botfather) в Telegram
   - `RAPID_API_KEY`: Получите ключ API
     у [@kinopoiskdev_bot](https://t.me/kinopoiskdev_bot)
5. Запустите бота: `python main.py`

## Использование

Отправьте команду `/start` боту в Telegram, чтобы начать взаимодействие. Используйте кнопки меню или команды для поиска
фильмов.
