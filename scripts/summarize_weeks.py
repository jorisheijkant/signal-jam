import os
from datetime import date, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.llm import get_llm_provider

PROMPT_PATH = Path(__file__).parent / 'prompts' / 'weekly_summary.txt'
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'ollama')


def get_monday(d: date) -> date:
    return d - timedelta(days=d.weekday())


def get_all_weeks_with_posts(conn) -> list[tuple[date, date]]:
    with conn.cursor() as cur:
        cur.execute("SELECT MIN(posted_at::date), MAX(posted_at::date) FROM posts")
        row = cur.fetchone()

    if not row or not row[0]:
        return []

    earliest, _ = row
    today = date.today()
    current_monday = get_monday(today)

    # Only summarize from 2026 onwards
    earliest = max(earliest, date(2026, 1, 1))

    weeks = []
    monday = get_monday(earliest)
    while monday < current_monday:
        sunday = monday + timedelta(days=6)
        weeks.append((monday, sunday))
        monday += timedelta(weeks=1)

    weeks.reverse()
    return weeks


def get_existing_summary_weeks(conn) -> set[date]:
    with conn.cursor() as cur:
        cur.execute("SELECT week_start FROM summaries")
        return {row[0] for row in cur.fetchall()}


def get_posts_for_week(conn, week_start: date, week_end: date) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.content, p.post_type, p.posted_at, p.platform,
                   a.username, a.display_name
            FROM posts p
            JOIN accounts a ON p.account_id = a.id
            WHERE p.posted_at::date BETWEEN %s AND %s
              AND p.content IS NOT NULL
              AND p.content != ''
            ORDER BY p.posted_at ASC
            """,
            (week_start, week_end),
        )
        cols = ['content', 'post_type', 'posted_at', 'platform', 'username', 'display_name']
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def format_posts_for_prompt(posts: list[dict]) -> str:
    lines = []
    for p in posts:
        name = p['display_name'] or p['username']
        date_str = p['posted_at'].strftime('%d-%m-%Y')
        post_type = f" [{p['post_type']}]" if p['post_type'] != 'original' else ''
        lines.append(f"[{date_str}] @{p['username']} ({name}){post_type}: {p['content']}")
    return '\n'.join(lines)


def insert_summary(conn, week_start: date, week_end: date, content: str, provider: str):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO summaries (week_start, week_end, content, llm_provider)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (week_start) DO UPDATE
              SET content = EXCLUDED.content,
                  llm_provider = EXCLUDED.llm_provider,
                  generated_at = NOW()
            """,
            (week_start, week_end, content, provider),
        )
    conn.commit()


def main():
    prompt_template = PROMPT_PATH.read_text(encoding='utf-8')

    print(f"Using LLM provider: {LLM_PROVIDER}")
    llm = get_llm_provider(LLM_PROVIDER)

    db = Database()

    all_weeks = get_all_weeks_with_posts(db.conn)
    existing = get_existing_summary_weeks(db.conn)
    pending = [(ws, we) for ws, we in all_weeks if ws not in existing]

    if not pending:
        print("All weeks already have a summary. Nothing to do.")
        return

    print(f"Found {len(pending)} week(s) without a summary.")

    for week_start, week_end in pending:
        print(f"\nGenerating summary for {week_start} – {week_end}...")

        posts = get_posts_for_week(db.conn, week_start, week_end)
        if not posts:
            print("  No posts found, skipping.")
            continue

        print(f"  {len(posts)} posts found.")

        posts_text = format_posts_for_prompt(posts)
        prompt = prompt_template.format(
            week_start=week_start.strftime('%d-%m-%Y'),
            week_end=week_end.strftime('%d-%m-%Y'),
            post_count=len(posts),
            posts=posts_text,
        )

        summary = llm.complete(prompt)
        insert_summary(db.conn, week_start, week_end, summary, LLM_PROVIDER)
        print(f"  Summary saved ({len(summary)} characters).")

    print("\nDone.")


if __name__ == '__main__':
    main()
