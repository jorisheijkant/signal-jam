def get_terms(conn, platform: str, kind: str) -> list[str]:
    """Terms of the given kind ('search' or 'filter') for the platform, oldest first."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT term FROM scrape_terms WHERE platform = %s AND kind = %s ORDER BY id",
            (platform, kind),
        )
        return [term for (term,) in cur.fetchall()]


def insert_terms(conn, platform: str, kind: str, terms: list[str]) -> None:
    """Add terms, skipping the ones that already exist."""
    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO scrape_terms (platform, kind, term)
            VALUES (%s, %s, %s)
            ON CONFLICT (platform, kind, term) DO NOTHING
            """,
            [(platform, kind, term) for term in terms],
        )
        conn.commit()
