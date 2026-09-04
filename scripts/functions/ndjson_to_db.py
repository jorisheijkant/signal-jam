import time

from functions.db_operations import upsert_account, insert_post, get_post_id_by_url
from functions.fact_checking import fact_check_post
from functions.llm import detect_language_with_llm

REQUIRED_LANGUAGE_ISO = 'nl'
RATE_LIMIT_REST_SECONDS = 120


def detect_post_language(llm, post):
    try:
        return detect_language_with_llm(llm, post.content).iso_639_1.lower()
    except Exception as e:
        print(f"  [language check failed] {post.url} — {e}")
        return None


def ndjson_to_db(conn, llm, ndjson_path, parse_ndjson, filter_terms=None, run_fact_check=False):
    """Parse an ndjson capture with parse_ndjson and insert the resulting posts into the database."""
    try:
        results = parse_ndjson(ndjson_path)
        print(f"Parsed {len(results)} posts, inserting into database...")

        for account, post in results:
            if filter_terms:
                content = (post.content or '').lower()
                if not any(term.lower() in content for term in filter_terms):
                    print(f"  [filtered] {account.username} — no filter term match, skipping")
                    continue

            post_language = detect_post_language(llm, post)
            if post_language != REQUIRED_LANGUAGE_ISO:
                print(f"  [skipped] {account.username} — language '{post_language}' is not Dutch")
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

            if post_id and run_fact_check:
                fact_check_post(conn, post_id, post.content)

        print("Now taking a 2 minute rest to avoid rate limiting")
        time.sleep(RATE_LIMIT_REST_SECONDS)
    except Exception as e:
        print(f"Something went wrong parsing the posts: {e}")
