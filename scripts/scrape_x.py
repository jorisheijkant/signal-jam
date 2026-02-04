import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from db import Database
from functions.setup_selenium import setup_selenium
from functions.x.scrape_term import scrape_term
from functions.x.scrape_x_profile import scrape_x_profile
from functions.x.ndjson_to_tweets import ndjson_to_tweets
from functions.db_operations import upsert_account, insert_post

x_term_search_url_base = "https://x.com/search?q="
x_term_search_url_affix = "%20lang%3Anl&src=typed_query"

x_users_to_scrape = [{
    "name": "Eric van de Beek 🇳 ",
    "url": "https://x.com/beek38"
}]

terms_to_scrape = ["rt.com"]

db = Database()
driver = setup_selenium()

def ndjson_to_db(ndjson_path):
    try:
        results = ndjson_to_tweets(ndjson_path)
        print(f"Parsed {len(results)} tweets, inserting into database...")

        for account, post in results:
            account_id = upsert_account(db.conn, account)
            post.account_id = account_id
            post_id = insert_post(db.conn, post)
            status = 'inserted' if post_id else 'already exists'
            print(f"  [{status}] {account.username} — {post.url}")

        # Wait 1 minute to avoid rate limiting
        current_time = datetime.now()
        time_hh_mm = current_time.strftime("%H:%M")
        print(f"Now taking a 1 minute rest to avoid rate limiting")
        time.sleep(60)
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
    user_ndjson_path = scrape_x_profile(driver, user["url"], user["name"])
    print(f"Written ndjson at {user_ndjson_path}")
    
    if user_ndjson_path:
        ndjson_to_db(user_ndjson_path)
