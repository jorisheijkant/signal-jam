import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.db_operations import get_watched_accounts, get_terms
from functions.setup_selenium import setup_selenium
from functions.scrape_url import scrape_url
from functions.ndjson_to_db import ndjson_to_db
from functions.x.ndjson_to_tweets import ndjson_to_tweets
from functions.llm import get_llm_provider
from functions.utils.pick_rotating_sample import pick_rotating_sample

X_PLATFORM = 'twitter'
X_PLATFORM_STATS_ID = 'twittercom'
X_SEARCH_URL_BASE = "https://x.com/search?q="
X_SEARCH_URL_AFFIX = "%20lang%3Anl&src=typed_query"
X_PROFILE_URL_SUFFIX = "/all"
SELENIUM_HEADLESS = True

LANGUAGE_DETECTION_PROVIDER = os.getenv('LANGUAGE_DETECTION_PROVIDER', 'ollama')

USERS_PER_RUN = 8
TERMS_PER_RUN = 2

BASE_DIR = Path(__file__).parent
ROTATION_STATE_PATH = BASE_DIR / 'data' / 'scrape_rotation_state.json'


def main():
    db = Database()
    all_x_users = get_watched_accounts(db.conn, X_PLATFORM)
    terms_to_scrape = get_terms(db.conn, X_PLATFORM, 'search')
    filter_terms = get_terms(db.conn, X_PLATFORM, 'filter')

    x_users_to_scrape = pick_rotating_sample(
        all_x_users, USERS_PER_RUN, ROTATION_STATE_PATH, 'users')
    terms_to_scrape = pick_rotating_sample(
        terms_to_scrape, TERMS_PER_RUN, ROTATION_STATE_PATH, 'terms')

    driver = setup_selenium(headless=SELENIUM_HEADLESS)
    llm = get_llm_provider(LANGUAGE_DETECTION_PROVIDER)

    try:
        for user_index, user in enumerate(x_users_to_scrape, 1):
            print(f"Now scraping user {user_index}/{len(x_users_to_scrape)}: {user['name']}")
            profile_url = user["url"].rstrip("/")

            user_ndjson_path = scrape_url(
                driver, f"{profile_url}{X_PROFILE_URL_SUFFIX}", user["name"], X_PLATFORM_STATS_ID)
            print(f"Written ndjson at {user_ndjson_path}")

            if user_ndjson_path:
                ndjson_to_db(
                    db.conn, llm, user_ndjson_path, ndjson_to_tweets,
                    filter_terms=filter_terms,
                )

        for term_index, term in enumerate(terms_to_scrape, 1):
            print(f"Now searching tweets containing term {term_index}/{len(terms_to_scrape)}: {term}")
            term_url = f"{X_SEARCH_URL_BASE}{term}{X_SEARCH_URL_AFFIX}"
            term_ndjson_path = scrape_url(driver, term_url, term, X_PLATFORM_STATS_ID)
            if term_ndjson_path:
                ndjson_to_db(
                    db.conn, llm, term_ndjson_path, ndjson_to_tweets,
                    required_search_term=term,
                )
    finally:
        driver.quit()
        print("Browser closed. All done.")


if __name__ == '__main__':
    main()
