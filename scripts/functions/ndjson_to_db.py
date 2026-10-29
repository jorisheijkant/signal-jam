import time

from functions.db_operations import upsert_account, is_account_approved, insert_post, get_post_id_by_url, record_repost
from functions.llm import detect_language_with_llm
from functions.utils.matches_filter_terms import matches_filter_terms
from functions.utils.contains_search_term import contains_search_term

REQUIRED_LANGUAGE_ISO = 'nl'
RATE_LIMIT_REST_SECONDS = 120


def detect_post_language(llm, post):
    try:
        return detect_language_with_llm(llm, post.content).iso_639_1.lower()
    except Exception as e:
        print(f"  [language check failed] {post.url} — {e}")
        return None


def handle_repost(conn, account, post):
    """Record that account reposted the original post, without creating a duplicate posts row."""
    original_post_id = get_post_id_by_url(conn, post.platform, post.parent_url)
    if not original_post_id:
        print(f"  [repost skipped] {account.username} — original post {post.parent_url} not yet in DB")
        return

    record_repost(conn, original_post_id, post.account_id, post.posted_at, post.url)
    print(f"  [repost recorded] {account.username} reposted post {original_post_id}")


def ndjson_to_db(conn, llm, ndjson_path, parse_ndjson, filter_terms=None, required_search_term=None):
    """Parse an ndjson capture with parse_ndjson and insert the resulting posts into the database.

    With required_search_term, posts that do not contain that term are dropped, since a capture
    also holds unrelated tweets from the rest of the page (sidebar, promoted posts)."""
    try:
        results = parse_ndjson(ndjson_path)
        print(f"Parsed {len(results)} posts, inserting into database...")

        for account, post in results:
            if post.post_type == 'reply':
                print(f"  [filtered] {account.username} — reply, skipping")
                continue

            if required_search_term and not contains_search_term(post, required_search_term):
                print(f"  [filtered] {account.username} — does not contain search term '{required_search_term}', skipping")
                continue

            post.relevant_for_signal_jam_theme = matches_filter_terms(post.content, filter_terms)
            if not post.relevant_for_signal_jam_theme and not is_account_approved(conn, account):
                print(f"  [filtered] {account.username} — no filter term match and account not approved, skipping")
                continue

            post_language = detect_post_language(llm, post)
            if post_language != REQUIRED_LANGUAGE_ISO:
                print(f"  [skipped] {account.username} — language '{post_language}' is not Dutch")
                continue

            post.account_id = upsert_account(conn, account)

            if post.post_type == 'repost':
                handle_repost(conn, account, post)
                continue

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
        time.sleep(RATE_LIMIT_REST_SECONDS)
    except Exception as e:
        print(f"Something went wrong parsing the posts: {e}")
