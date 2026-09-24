import os
from datetime import date, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.llm import get_llm_provider
from functions.source_desk import load_articles_for_week

# Also summarize source-desk's Russian propaganda channel articles for each week.
# Requires SOURCE_DESK_ARTICLES_DIR to point at source-desk's exported article JSON files.
GENERATE_PROPAGANDA_SUMMARY = True

PROMPT_PATH = Path(__file__).parent / 'prompts' / 'weekly_summary.txt'
PROPAGANDA_PROMPT_PATH = Path(__file__).parent / 'prompts' / 'weekly_propaganda_summary.txt'
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'ollama')
ARTICLES_DIR = Path(os.getenv('SOURCE_DESK_ARTICLES_DIR', ''))
MAX_ARTICLE_CHARS = 600


def get_monday(day: date) -> date:
    return day - timedelta(days=day.weekday())


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


def get_summary_status_by_week(conn) -> dict[date, bool]:
    """Map week_start to whether that week's propaganda summary has already been checked.

    propaganda_channels_content is NULL until a check has run, then either holds the
    generated summary or an empty string if the check found no articles for that week.
    Either way, NOT NULL means "already checked" and the week should not be re-queued.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT week_start, propaganda_channels_content IS NOT NULL FROM summaries")
        return dict(cur.fetchall())


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


def format_articles_for_prompt(articles: list[dict]) -> str:
    lines = []
    for article in articles:
        date_str = article['published_at'][:10]
        text = (article.get('summary') or article.get('content') or '')[:MAX_ARTICLE_CHARS]
        lines.append(f"[{date_str}] {article['source']} — {article['title']}: {text}")
    return '\n'.join(lines)


def generate_propaganda_summary(llm, prompt_template: str, week_start: date, week_end: date) -> str | None:
    """Summarize source-desk's Russian propaganda channel articles for the week, or None if there's nothing to summarize."""
    articles = load_articles_for_week(ARTICLES_DIR, week_start, week_end)
    if not articles:
        return None

    prompt = prompt_template.format(
        week_start=week_start.strftime('%d-%m-%Y'),
        week_end=week_end.strftime('%d-%m-%Y'),
        article_count=len(articles),
        articles=format_articles_for_prompt(articles),
    )
    return llm.complete(prompt)


def insert_summary(conn, week_start: date, week_end: date, content: str, provider: str, propaganda_content: str | None = None):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO summaries (week_start, week_end, content, propaganda_channels_content, llm_provider)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (week_start) DO UPDATE
              SET content = EXCLUDED.content,
                  propaganda_channels_content = COALESCE(EXCLUDED.propaganda_channels_content, summaries.propaganda_channels_content),
                  llm_provider = EXCLUDED.llm_provider,
                  generated_at = NOW()
            """,
            (week_start, week_end, content, propaganda_content, provider),
        )
    conn.commit()


def update_propaganda_summary(conn, week_start: date, content: str):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE summaries SET propaganda_channels_content = %s WHERE week_start = %s",
            (content, week_start),
        )
    conn.commit()


def process_week(conn, llm, prompt_template, propaganda_prompt_template, week_start: date, week_end: date, has_summary: bool, needs_propaganda_summary: bool):
    content = None
    if not has_summary:
        posts = get_posts_for_week(conn, week_start, week_end)
        if not posts:
            print("  No posts found, skipping.")
            return

        print(f"  {len(posts)} posts found.")
        posts_text = format_posts_for_prompt(posts)
        prompt = prompt_template.format(
            week_start=week_start.strftime('%d-%m-%Y'),
            week_end=week_end.strftime('%d-%m-%Y'),
            post_count=len(posts),
            posts=posts_text,
        )
        content = llm.complete(prompt)

    propaganda_content = None
    if needs_propaganda_summary:
        propaganda_content = generate_propaganda_summary(llm, propaganda_prompt_template, week_start, week_end)
        if propaganda_content:
            print(f"  Propaganda summary generated ({len(propaganda_content)} characters).")
        else:
            print("  No propaganda articles found for this week, marking as checked.")
            propaganda_content = ''

    if content is not None:
        insert_summary(conn, week_start, week_end, content, LLM_PROVIDER, propaganda_content)
        print(f"  Summary saved ({len(content)} characters).")
    elif propaganda_content is not None:
        update_propaganda_summary(conn, week_start, propaganda_content)
        print("  Propaganda summary saved.")


def main():
    if GENERATE_PROPAGANDA_SUMMARY and not ARTICLES_DIR.is_dir():
        print(f"GENERATE_PROPAGANDA_SUMMARY is on but SOURCE_DESK_ARTICLES_DIR is not a directory: {ARTICLES_DIR}")
        return

    prompt_template = PROMPT_PATH.read_text(encoding='utf-8')
    propaganda_prompt_template = PROPAGANDA_PROMPT_PATH.read_text(encoding='utf-8') if GENERATE_PROPAGANDA_SUMMARY else None

    print(f"Using LLM provider: {LLM_PROVIDER}")
    llm = get_llm_provider(LLM_PROVIDER)

    db = Database()

    all_weeks = get_all_weeks_with_posts(db.conn)
    summary_status = get_summary_status_by_week(db.conn)

    pending = [
        (week_start, week_end) for week_start, week_end in all_weeks
        if week_start not in summary_status
        or (GENERATE_PROPAGANDA_SUMMARY and not summary_status[week_start])
    ]

    if not pending:
        print("All weeks already have a summary. Nothing to do.")
        return

    print(f"Found {len(pending)} week(s) needing work.")

    for week_start, week_end in pending:
        has_summary = week_start in summary_status
        needs_propaganda_summary = GENERATE_PROPAGANDA_SUMMARY and not summary_status.get(week_start, False)

        print(f"\nProcessing {week_start} – {week_end}...")

        try:
            process_week(db.conn, llm, prompt_template, propaganda_prompt_template, week_start, week_end, has_summary, needs_propaganda_summary)
        except Exception as e:
            print(f"  [failed] {week_start} – {week_end}: {e}")
            db.conn.rollback()

    print("\nDone.")


if __name__ == '__main__':
    main()
