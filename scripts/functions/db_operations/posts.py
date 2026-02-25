import json
from classes import Post


def has_post_today(conn, platform: str, username: str) -> bool:
    """Return True if there is already a post from this account scraped today."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM posts p
                JOIN accounts a ON p.account_id = a.id
                WHERE a.platform = %s
                  AND LOWER(a.username) = LOWER(%s)
                  AND p.posted_at >= CURRENT_DATE
            )
            """,
            (platform, username),
        )
        return cur.fetchone()[0]


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
