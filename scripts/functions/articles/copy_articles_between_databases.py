from datetime import timezone

BATCH_SIZE = 500
COLUMNS = ['url', 'title', 'source', 'author', 'language', 'summary', 'content', 'published_at', 'scraped_at']


def copy_articles_between_databases(source_conn, target_conn, is_dry_run: bool = False) -> int:
    """Upsert every article from source_conn into target_conn, returns the number of rows read.

    Source Desk stored timestamps without a timezone, always in UTC, so they are tagged as UTC here.
    """
    with source_conn.cursor(name='read_articles') as source_cur:
        source_cur.itersize = BATCH_SIZE
        source_cur.execute(f"SELECT {', '.join(COLUMNS)} FROM articles ORDER BY published_at")
        copied = 0
        batch = []
        for row in source_cur:
            batch.append(_tag_timestamps_as_utc(dict(zip(COLUMNS, row))))
            if len(batch) == BATCH_SIZE:
                copied += _flush(target_conn, batch, is_dry_run)
                batch = []
        copied += _flush(target_conn, batch, is_dry_run)
    return copied


def _tag_timestamps_as_utc(article: dict) -> dict:
    for column in ('published_at', 'scraped_at'):
        article[column] = article[column].replace(tzinfo=timezone.utc)
    return article


def _flush(target_conn, batch: list[dict], is_dry_run: bool) -> int:
    if not batch or is_dry_run:
        return len(batch)
    with target_conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO articles (url, title, source, author, language, summary, content, published_at, scraped_at)
            VALUES (%(url)s, %(title)s, %(source)s, %(author)s, %(language)s, %(summary)s, %(content)s, %(published_at)s, %(scraped_at)s)
            ON CONFLICT (url) DO NOTHING
            """,
            batch,
        )
    target_conn.commit()
    return len(batch)
