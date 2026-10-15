def find_existing_urls(conn, urls: list[str]) -> set[str]:
    with conn.cursor() as cur:
        cur.execute("SELECT url FROM articles WHERE url = ANY(%s)", (urls,))
        return {row[0] for row in cur.fetchall()}
