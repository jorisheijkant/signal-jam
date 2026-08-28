import json
from datetime import datetime, timezone

from classes import Account, Post

INSTAGRAM_POST_URL_BASE = "https://www.instagram.com/p/"


def _extract_engagement(item, typename):
    """Instagram's raw API responses come in three shapes depending on which page
    served them: 'Polaris' (the modern app API, seen on some partial listing pages
    like tagged/popular views), 'Graph' (the legacy shape, e.g. single-post pages),
    and a generic itemlist shape used elsewhere (e.g. search results, reels).
    Only Graph and itemlist items expose like/comment counts and a real timestamp
    in what gets captured — Polaris items never do, so those fall back to 0
    engagement and "now" as posted_at rather than being skipped entirely.
    """
    is_polaris = isinstance(typename, str) and 'polaris' in typename.lower()
    is_graph = isinstance(typename, str) and typename != 'XDTMediaDict'

    if is_polaris:
        return 0, 0, None

    likes_disabled = bool(item.get('like_and_view_counts_disabled'))

    if is_graph:
        likes = 0 if likes_disabled else (item.get('edge_media_preview_like') or {}).get('count', 0)
        comments = (item.get('edge_media_preview_comment') or {}).get('count', 0)
        posted_at_unix = item.get('taken_at_timestamp')
    else:
        likes = 0 if likes_disabled else item.get('like_count', 0)
        if 'comment_count' in item:
            comments = item.get('comment_count', 0)
        elif isinstance(item.get('comments'), list):
            comments = len(item['comments'])
        else:
            comments = 0
        posted_at_unix = None if item.get('_zs_partial') else item.get('taken_at')

    return likes or 0, comments or 0, posted_at_unix


def _posted_at(unix_seconds):
    if not unix_seconds:
        return datetime.now(tz=timezone.utc)
    try:
        return datetime.fromtimestamp(int(unix_seconds), tz=timezone.utc)
    except (ValueError, TypeError):
        return datetime.now(tz=timezone.utc)


def ndjson_to_instagram_posts(ndjson_path):
    results = []

    with open(ndjson_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            try:
                entry = json.loads(line)
                item = entry.get('data', {})

                shortcode = item.get('code') or item.get('shortcode')
                user = item.get('user') or {}
                owner = item.get('owner') or {}
                username = user.get('username') or owner.get('username')

                if not shortcode or not username:
                    continue

                display_name = user.get('full_name') or owner.get('full_name')
                caption = item.get('caption')
                content = caption.get('text') if isinstance(caption, dict) else None

                account = Account(
                    platform='instagram',
                    username=username,
                    account_url=f"https://www.instagram.com/{username}/",
                    display_name=(display_name or '').strip() or None,
                )

                likes, comments, posted_at_unix = _extract_engagement(item, item.get('__typename'))

                # Instagram's reshare feature has no confirmed field for linking a
                # repost back to its original post in the captured data, so every
                # item lands as 'original' for now — same known-gap approach as
                # TikTok duets (see ndjson_to_tiktoks.py).
                post = Post(
                    platform='instagram',
                    account_id=None,
                    posted_at=_posted_at(posted_at_unix),
                    url=f"{INSTAGRAM_POST_URL_BASE}{shortcode}",
                    content=content,
                    post_type='original',
                    likes=likes,
                    reposts=0,
                    comments=comments,
                    platform_data=entry,
                )

                results.append((account, post))
            except json.JSONDecodeError:
                continue

    return results
