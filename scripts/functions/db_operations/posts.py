import json
from classes import Post


def get_post_id_by_url(conn, platform: str, url: str) -> int | None:
    """Return the DB id of a post by its platform + URL, or None if not found."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM posts WHERE platform = %s AND url = %s",
            (platform, url),
        )
        row = cur.fetchone()
        return row[0] if row else None


def delete_posts_scraped_in_last_days(conn, days: int) -> int:
    """Delete posts scraped within the last `days` days. Returns the number of deleted rows."""
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM posts WHERE scraped_at >= NOW() - INTERVAL '%s days'",
            (days,),
        )
        conn.commit()
        return cur.rowcount


def insert_post(conn, post: Post) -> int:
    """Insert a post, skipping on (platform, url) conflict. Returns the post id."""
    platform_data = json.dumps(post.platform_data) if post.platform_data else None

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO posts (
                url, platform, account_id, content, post_type,
                parent_post_id, posted_at, likes, reposts, comments,
                is_checked, contains_misinformation, platform_data
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (platform, url) DO NOTHING
            RETURNING id
            """,
            (
                post.url, post.platform, post.account_id, post.content,
                post.post_type, post.parent_post_id, post.posted_at,
                post.likes, post.reposts, post.comments,
                post.is_checked, post.contains_misinformation, platform_data,
            ),
        )
        conn.commit()
        row = cur.fetchone()
        return row[0] if row else None
