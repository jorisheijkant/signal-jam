import json
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from db import Database
from functions.setup_selenium import setup_selenium
from functions.x.scrape_term import scrape_term
from functions.x.scrape_x_profile import scrape_x_profile
from functions.x.ndjson_to_tweets import ndjson_to_tweets
from functions.db_operations import upsert_account, insert_post, has_post_today

x_term_search_url_base = "https://x.com/search?q="
x_term_search_url_affix = "%20lang%3Anl&src=typed_query"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

x_users_to_scrape = load_json('source_data/x_users_to_scrape.json')
terms_to_scrape = load_json('source_data/terms_to_scrape.json')
filter_terms = load_json('source_data/filter_terms.json')

db = Database()
driver = setup_selenium()

def ndjson_to_db(ndjson_path, filter_terms=None):
    try:
        results = ndjson_to_tweets(ndjson_path)
        print(f"Parsed {len(results)} tweets, inserting into database...")

        for account, post in results:
            if filter_terms:
                content = post.content or ''
                content_lower = content.lower()
                if not any(term.lower() in content_lower for term in filter_terms):
                    print(f"  [filtered] {account.username} — no filter term match, skipping")
                    continue

            account_id = upsert_account(db.conn, account)
            post.account_id = account_id
            post_id = insert_post(db.conn, post)
            status = 'inserted' if post_id else 'already exists'
            print(f"  [{status}] {account.username} — {post.url}")

        # Wait 1 minute to avoid rate limiting
        current_time = datetime.now()
        time_hh_mm = current_time.strftime("%H:%M")
        print(f"Now taking a 2 minute rest to avoid rate limiting")
        time.sleep(120)
    except Exception as e:
        print(f"Something went wrong parsing the tweets: {e}")

for term_index, term in enumerate(terms_to_scrape, 1):
    print(f"Now searching tweets containing term {term_index}/{len(terms_to_scrape)}: {term}")
    term_url = f"{x_term_search_url_base}{term}{x_term_search_url_affix}"
    term_ndjson_path = scrape_term(driver, term_url, term)
    if term_ndjson_path:
        ndjson_to_db(term_ndjson_path)

for user_index, user in enumerate(x_users_to_scrape, 1):
    print(f"Now scraping user {user_index}/{len(x_users_to_scrape)}: {user['name']}")
    username = user["url"].rstrip("/").split("/")[-1]

    if has_post_today(db.conn, "twitter", username):
        print(f"  [skipped] {user['name']} already has a post from today in the database")
        continue

    user_ndjson_path = scrape_x_profile(driver, user["url"], user["name"])
    print(f"Written ndjson at {user_ndjson_path}")

    if user_ndjson_path:
        ndjson_to_db(user_ndjson_path, filter_terms=filter_terms)

driver.quit()
print("Browser closed. All done.")
