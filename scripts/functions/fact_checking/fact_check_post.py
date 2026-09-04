import asyncio

from functions.db_operations import save_ai_fact_check
from functions.fact_checking.fact_check_with_claude import MODEL, fact_check_with_claude


def fact_check_post(conn, post_id: int, content: str) -> None:
    """Run an AI fact-check on a post's content and store the suggestion, if any."""
    if not content:
        return

    try:
        result = asyncio.run(fact_check_with_claude(content))
    except Exception as e:
        print(f"  [fact check failed] post {post_id} — {e}")
        return

    if not result:
        return

    try:
        save_ai_fact_check(conn, post_id, MODEL, result)
    except Exception as e:
        conn.rollback()
        print(f"  [fact check not saved] post {post_id} — {e}")
        return

    print(f"  [fact checked] post {post_id} — likely_disinformation={result['likely_disinformation']}")
