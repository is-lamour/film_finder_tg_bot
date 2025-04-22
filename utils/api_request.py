import requests
import json
import logging
from config_data.config import RAPID_API_KEY
from database.history_db import save_to_history

logging.basicConfig(level=logging.INFO)

def search_movie_by_title(title):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=5&query={title}"
    try:
        return make_api_request(url)
    except Exception as e:
        logging.error(f"Error in search_movie_by_title: {e}")
        return None

def search_movie_by_rating(rating):
    try:
        tuple_rating = tuple(map(float, rating.split()))
        url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit=5&rating.kp={tuple_rating[0]}&rating.kp={tuple_rating[-1]}"
        return make_api_request(url)
    except ValueError as e:
        logging.error(f"Error in search_movie_by_rating: Invalid rating format - {e}")
        return None

def search_low_budget_movies():
    url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit=5&budget.value={1_000_000}"
    return make_api_request(url)

def search_high_budget_movies():
    url = f"https://api.kinopoisk.dev/v1.4/movie?page=1&limit=5&budget.value={100_000_000}"
    return make_api_request(url)

def make_api_request(url):
    headers = {
        "accept": "application/json",
        "X-API-KEY": RAPID_API_KEY
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        json_dict = response.json()

        if 'docs' in json_dict and json_dict['docs']:
            for movie in json_dict['docs']:
                try:
                    save_to_history(movie)
                except Exception as e:
                    logging.error(f"Error saving to history: {e}")
            return json_dict['docs']
        else:
            logging.info(f"No results found for URL: {url}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON response: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in make_api_request: {e}")
        return None
