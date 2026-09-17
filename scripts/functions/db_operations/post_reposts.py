def record_repost(conn, post_id: int, account_id: int, reposted_at, url: str | None) -> None:
    """Record that an account reposted a post, updating the timestamp/url on conflict."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO post_reposts (post_id, account_id, reposted_at, url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (post_id, account_id) DO UPDATE SET
                reposted_at = EXCLUDED.reposted_at,
                url = COALESCE(EXCLUDED.url, post_reposts.url)
            """,
            (post_id, account_id, reposted_at, url),
        )
        conn.commit()
