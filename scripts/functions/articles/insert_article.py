def insert_article(conn, article: dict) -> bool:
    """Insert an article, skipping it if the url already exists. Returns whether a row was added."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO articles (url, title, source, author, language, summary, content, published_at, relevant_for_signal_jam_theme)
            VALUES (%(url)s, %(title)s, %(source)s, %(author)s, %(language)s, %(summary)s, %(content)s, %(published_at)s, %(relevant_for_signal_jam_theme)s)
            ON CONFLICT (url) DO NOTHING
            """,
            article,
        )
        conn.commit()
        return cur.rowcount == 1
