"""AI fact-check the newest N posts already in the database that don't have one yet.

Run this on a schedule (see scripts/README.md) rather than fact-checking inline
during scraping, to keep scrape runs fast and to control fact-check API spend.

Usage: python backfill_fact_checks.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

# claude_agent_sdk authenticates via the Claude Code CLI session by default, but
# switches to API-key billing if it sees this in the environment. Keep it out so
# this script never bills against ANTHROPIC_API_KEY, even though the shared
# .env defines it (summarize_weeks.py needs it for its own Anthropic client).
os.environ.pop('ANTHROPIC_API_KEY', None)

from db import Database
from functions.fact_checking import MODEL, fact_check_post

POST_LIMIT = 100


def fetch_newest_posts(conn, limit, provider):
    """Newest posts that still need an AI fact-check: no human review yet, and no
    existing AI fact-check from this provider (so re-running the script is a no-op)."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.id, p.content FROM posts p
            WHERE p.content IS NOT NULL
              AND p.is_checked = FALSE
              AND NOT EXISTS (
                  SELECT 1 FROM ai_fact_checks afc
                  WHERE afc.post_id = p.id AND afc.provider = %s
              )
            ORDER BY p.scraped_at DESC
            LIMIT %s
            """,
            (provider, limit),
        )
        return cur.fetchall()


def main():
    db = Database()
    posts = fetch_newest_posts(db.conn, POST_LIMIT, MODEL)
    print(f"Fact-checking {len(posts)} posts...")

    for index, (post_id, content) in enumerate(posts, 1):
        print(f"[{index}/{len(posts)}] post {post_id}")
        fact_check_post(db.conn, post_id, content)


if __name__ == '__main__':
    main()
