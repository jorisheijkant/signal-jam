import json
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.setup_selenium import setup_selenium
from functions.x.scrape_url import scrape_url
from functions.x.ndjson_to_tweets import ndjson_to_tweets
from functions.db_operations import upsert_account, insert_post, has_post_today, get_post_id_by_url

X_SEARCH_URL_BASE = "https://x.com/search?q="
X_SEARCH_URL_AFFIX = "%20lang%3Anl&src=typed_query"

BASE_DIR = Path(__file__).parent


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def ndjson_to_db(conn, ndjson_path, filter_terms=None):
    try:
        results = ndjson_to_tweets(ndjson_path)
        print(f"Parsed {len(results)} tweets, inserting into database...")

        for account, post in results:
            if filter_terms:
                content = (post.content or '').lower()
                if not any(term.lower() in content for term in filter_terms):
                    print(f"  [filtered] {account.username} — no filter term match, skipping")
                    continue

            post.account_id = upsert_account(conn, account)

            if post.parent_url and post.parent_post_id is None:
                post.parent_post_id = get_post_id_by_url(conn, post.platform, post.parent_url)
                if post.parent_post_id:
                    print(f"  [parent resolved] {post.parent_url} → id {post.parent_post_id}")
                else:
                    print(f"  [parent not found] {post.parent_url} (not yet in DB)")

            post_id = insert_post(conn, post)
            status = 'inserted' if post_id else 'already exists'
            print(f"  [{status}] {account.username} — {post.url}")

        print("Now taking a 2 minute rest to avoid rate limiting")
        time.sleep(120)
    except Exception as e:
        print(f"Something went wrong parsing the tweets: {e}")


def main():
    x_users_to_scrape = load_json(BASE_DIR / 'source_data/x_users_to_scrape.json')
    terms_to_scrape = load_json(BASE_DIR / 'source_data/terms_to_scrape.json')
    filter_terms = load_json(BASE_DIR / 'source_data/filter_terms.json')

    db = Database()
    driver = setup_selenium()

    try:
        for term_index, term in enumerate(terms_to_scrape, 1):
            print(f"Now searching tweets containing term {term_index}/{len(terms_to_scrape)}: {term}")
            term_url = f"{X_SEARCH_URL_BASE}{term}{X_SEARCH_URL_AFFIX}"
            term_ndjson_path = scrape_url(driver, term_url, term)
            if term_ndjson_path:
                ndjson_to_db(db.conn, term_ndjson_path)

        for user_index, user in enumerate(x_users_to_scrape, 1):
            print(f"Now scraping user {user_index}/{len(x_users_to_scrape)}: {user['name']}")
            username = user["url"].rstrip("/").split("/")[-1]

            if has_post_today(db.conn, "twitter", username):
                print(f"  [skipped] {user['name']} already has a post from today in the database")
                continue

            user_ndjson_path = scrape_url(driver, user["url"], user["name"])
            print(f"Written ndjson at {user_ndjson_path}")

            if user_ndjson_path:
                ndjson_to_db(db.conn, user_ndjson_path, filter_terms=filter_terms)
    finally:
        driver.quit()
        print("Browser closed. All done.")


if __name__ == '__main__':
    main()
