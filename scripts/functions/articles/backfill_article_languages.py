def backfill_article_languages(conn, sources: list[dict]) -> int:
    """Set the language of every stored article to the language configured for its source, returns the rows updated."""
    updated_count = 0
    with conn.cursor() as cur:
        for source in sources:
            cur.execute(
                "UPDATE articles SET language = %s WHERE source = %s AND language IS DISTINCT FROM %s",
                (source['language'], source['name'], source['language']),
            )
            updated_count += cur.rowcount
    conn.commit()
    return updated_count
