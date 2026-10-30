import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.db_operations import get_watched_accounts, get_terms
from functions.setup_selenium import setup_selenium
from functions.scrape_url import scrape_url
from functions.ndjson_to_db import ndjson_to_db
from functions.tiktok.ndjson_to_tiktoks import ndjson_to_tiktoks
from functions.tiktok.retry_on_load_error import retry_on_load_error
from functions.llm import get_llm_provider
from functions.utils.pick_rotating_sample import pick_rotating_sample

TIKTOK_PLATFORM = 'tiktok'
TIKTOK_PLATFORM_STATS_ID = 'tiktokcom'
TIKTOK_SEARCH_URL_BASE = "https://www.tiktok.com/search?q="
SELENIUM_HEADLESS = True

LANGUAGE_DETECTION_PROVIDER = os.getenv('LANGUAGE_DETECTION_PROVIDER', 'ollama')

USERS_PER_RUN = 8
TERMS_PER_RUN = 2

BASE_DIR = Path(__file__).parent
ROTATION_STATE_PATH = BASE_DIR / 'data' / 'tiktok_scrape_rotation_state.json'


def main():
    db = Database()
    all_tiktok_users = get_watched_accounts(db.conn, TIKTOK_PLATFORM)
    terms_to_scrape = get_terms(db.conn, TIKTOK_PLATFORM, 'search')
    filter_terms = get_terms(db.conn, TIKTOK_PLATFORM, 'filter')

    tiktok_users_to_scrape = pick_rotating_sample(
        all_tiktok_users, USERS_PER_RUN, ROTATION_STATE_PATH, 'users')
    terms_to_scrape = pick_rotating_sample(
        terms_to_scrape, TERMS_PER_RUN, ROTATION_STATE_PATH, 'terms')

    driver = setup_selenium(headless=SELENIUM_HEADLESS)
    llm = get_llm_provider(LANGUAGE_DETECTION_PROVIDER)

    try:
        for user_index, user in enumerate(tiktok_users_to_scrape, 1):
            print(f"Now scraping user {user_index}/{len(tiktok_users_to_scrape)}: {user['name']}")
            profile_url = user["url"].rstrip("/")

            user_ndjson_path = scrape_url(
                driver, profile_url, user["name"], TIKTOK_PLATFORM_STATS_ID, on_scroll=retry_on_load_error)
            print(f"Written ndjson at {user_ndjson_path}")

            if user_ndjson_path:
                ndjson_to_db(
                    db.conn, llm, user_ndjson_path, ndjson_to_tiktoks,
                    filter_terms=filter_terms,
                )

        for term_index, term in enumerate(terms_to_scrape, 1):
            print(f"Now searching videos containing term {term_index}/{len(terms_to_scrape)}: {term}")
            term_url = f"{TIKTOK_SEARCH_URL_BASE}{term}"
            term_ndjson_path = scrape_url(
                driver, term_url, term, TIKTOK_PLATFORM_STATS_ID, on_scroll=retry_on_load_error)
            if term_ndjson_path:
                ndjson_to_db(
                    db.conn, llm, term_ndjson_path, ndjson_to_tiktoks,
                    required_search_term=term,
                )
    finally:
        driver.quit()
        print("Browser closed. All done.")


if __name__ == '__main__':
    main()
