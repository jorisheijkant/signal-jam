import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from classes import Account
from db import Database
from functions.db_operations import watch_account, insert_terms
from functions.utils.username_from_profile_url import username_from_profile_url

SOURCE_DATA_DIR = Path(__file__).parent / 'source_data'

SOURCE_FILES_PER_PLATFORM = {
    'twitter': {
        'users': 'x/x_users_to_scrape.json',
        'search': 'x/terms_to_scrape.json',
        'filter': 'x/filter_terms.json',
    },
    'tiktok': {
        'users': 'tiktok/tiktok_users_to_scrape.json',
        'search': 'tiktok/tiktok_terms_to_scrape.json',
        'filter': 'tiktok/filter_terms.json',
    },
    'instagram': {
        'users': 'instagram/instagram_users_to_scrape.json',
        'search': 'instagram/instagram_terms_to_scrape.json',
        'filter': 'instagram/filter_terms.json',
    },
}


def load_json_if_present(relative_path):
    path = SOURCE_DATA_DIR / relative_path
    if not path.exists():
        print(f"[skipped] {path} not found")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def import_users(conn, platform, users):
    for user in users:
        username = username_from_profile_url(platform, user['url'])
        if not username:
            print(f"[skipped] Could not read a username from {user['url']}")
            continue
        watch_account(conn, Account(
            platform=platform,
            username=username,
            account_url=user['url'].rstrip('/'),
            display_name=user.get('name'),
        ))
        print(f"Watching {platform}: {username}")


def import_terms(conn, platform, kind, terms):
    insert_terms(conn, platform, kind, terms)
    print(f"Imported {len(terms)} {kind} terms for {platform}")


def main():
    db = Database()
    for platform, files in SOURCE_FILES_PER_PLATFORM.items():
        import_users(db.conn, platform, load_json_if_present(files['users']))
        import_terms(db.conn, platform, 'search', load_json_if_present(files['search']))
        import_terms(db.conn, platform, 'filter', load_json_if_present(files['filter']))


if __name__ == '__main__':
    main()
