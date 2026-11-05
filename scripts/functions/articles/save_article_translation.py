def save_article_translation(conn, url: str, title_en: str, content_en: str | None) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE articles SET title_en = %s, content_en = %s WHERE url = %s",
            (title_en, content_en, url),
        )
    conn.commit()
