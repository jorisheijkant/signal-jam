def fetch_untranslated_articles(conn, languages: list[str], limit: int) -> list[dict]:
    """Articles in one of the given languages without an English title yet, relevant ones first, then newest first."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT url, title, content, language
            FROM articles
            WHERE language = ANY(%s) AND title_en IS NULL
            ORDER BY relevant_for_signal_jam_theme DESC, published_at DESC
            LIMIT %s
            """,
            (languages, limit),
        )
        columns = [column.name for column in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
