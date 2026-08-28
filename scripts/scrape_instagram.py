import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.setup_selenium import setup_selenium
from functions.scrape_url import scrape_url
from functions.ndjson_to_db import ndjson_to_db
from functions.instagram.ndjson_to_instagram_posts import ndjson_to_instagram_posts
from functions.llm import get_llm_provider
from functions.utils.pick_rotating_sample import pick_rotating_sample

INSTAGRAM_PLATFORM_STATS_ID = 'instagramcom'
INSTAGRAM_SEARCH_URL_BASE = "https://www.instagram.com/explore/search/keyword/?q="
SELENIUM_HEADLESS = True

LANGUAGE_DETECTION_PROVIDER = os.getenv('LANGUAGE_DETECTION_PROVIDER', 'ollama')

USERS_PER_RUN = 8
TERMS_PER_RUN = 2

BASE_DIR = Path(__file__).parent
SOURCE_DATA_DIR = BASE_DIR / 'source_data' / 'instagram'
ROTATION_STATE_PATH = BASE_DIR / 'data' / 'instagram_scrape_rotation_state.json'


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    instagram_users_to_scrape = load_json(SOURCE_DATA_DIR / 'instagram_users_to_scrape.json')
    terms_to_scrape = load_json(SOURCE_DATA_DIR / 'instagram_terms_to_scrape.json')
    filter_terms = load_json(SOURCE_DATA_DIR / 'filter_terms.json')

    instagram_users_to_scrape = pick_rotating_sample(
        instagram_users_to_scrape, USERS_PER_RUN, ROTATION_STATE_PATH, 'users')
    terms_to_scrape = pick_rotating_sample(
        terms_to_scrape, TERMS_PER_RUN, ROTATION_STATE_PATH, 'terms')

    db = Database()
    driver = setup_selenium(headless=SELENIUM_HEADLESS)
    llm = get_llm_provider(LANGUAGE_DETECTION_PROVIDER)

    try:
        for user_index, user in enumerate(instagram_users_to_scrape, 1):
            print(f"Now scraping user {user_index}/{len(instagram_users_to_scrape)}: {user['name']}")
            profile_url = user["url"].rstrip("/")

            user_ndjson_path = scrape_url(
                driver, profile_url, user["name"], INSTAGRAM_PLATFORM_STATS_ID)
            print(f"Written ndjson at {user_ndjson_path}")

            if user_ndjson_path:
                ndjson_to_db(db.conn, llm, user_ndjson_path, ndjson_to_instagram_posts, filter_terms=filter_terms)

        for term_index, term in enumerate(terms_to_scrape, 1):
            print(f"Now searching posts containing term {term_index}/{len(terms_to_scrape)}: {term}")
            term_url = f"{INSTAGRAM_SEARCH_URL_BASE}{term}"
            term_ndjson_path = scrape_url(driver, term_url, term, INSTAGRAM_PLATFORM_STATS_ID)
            if term_ndjson_path:
                ndjson_to_db(db.conn, llm, term_ndjson_path, ndjson_to_instagram_posts)
    finally:
        driver.quit()
        print("Browser closed. All done.")


if __name__ == '__main__':
    main()
