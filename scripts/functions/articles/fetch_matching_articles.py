from datetime import date


def fetch_matching_articles(conn, terms: list[str], start_date: date, end_date: date) -> list[dict]:
    """Articles published in [start_date, end_date] whose title, summary or content mention any search term."""
    term_condition = " OR ".join(["title ILIKE %s OR summary ILIKE %s OR content ILIKE %s"] * len(terms))
    term_params = [f"%{term}%" for term in terms for _ in range(3)]

    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT url, title, source, published_at, summary, content
            FROM articles
            WHERE published_at::date BETWEEN %s AND %s
              AND ({term_condition})
            ORDER BY published_at ASC
            """,
            [start_date, end_date, *term_params],
        )
        columns = [column.name for column in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
