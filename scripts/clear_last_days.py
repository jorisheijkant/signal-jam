from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.db_operations import delete_posts_scraped_in_last_days

amount_of_days = 7


def main():
    db = Database()
    deleted = delete_posts_scraped_in_last_days(db.conn, amount_of_days)
    print(f"Deleted {deleted} post(s) scraped in the last {amount_of_days} day(s).")


if __name__ == '__main__':
    main()
