from functions.articles.matches_article_filter_terms import matches_article_filter_terms


def flag_existing_articles(conn, filter_terms: list[str]) -> int:
    """Recompute the theme flag of every stored article, returns the number of articles flagged as relevant."""
    with conn.cursor() as cur:
        cur.execute("SELECT url, title, summary, content FROM articles")
        columns = [column.name for column in cur.description]
        articles = [dict(zip(columns, row)) for row in cur.fetchall()]

        relevant_urls = [a['url'] for a in articles if matches_article_filter_terms(a, filter_terms)]
        cur.execute("UPDATE articles SET relevant_for_signal_jam_theme = (url = ANY(%s))", (relevant_urls,))
    conn.commit()
    return len(relevant_urls)
