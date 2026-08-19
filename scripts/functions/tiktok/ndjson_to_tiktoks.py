import json
from datetime import datetime, timezone

from classes import Account, Post


def ndjson_to_tiktoks(ndjson_path):
    results = []

    with open(ndjson_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            try:
                entry = json.loads(line)
                item = entry.get('data', {})

                video_id = item.get('id')
                author = item.get('author', {})
                username = author.get('uniqueId') if isinstance(author, dict) else author

                if not video_id or not username:
                    continue

                display_name = author.get('nickname') if isinstance(author, dict) else item.get('nickname')

                account = Account(
                    platform='tiktok',
                    username=username,
                    account_url=f"https://www.tiktok.com/@{username}",
                    display_name=(display_name or '').strip() or None,
                )

                # Duets add original content alongside a reference to another video, closest
                # to X's "quote" concept. The captured data only exposes the referenced video's
                # id (duetFromId), not its author, so the parent link can't be resolved.
                duet_from_id = (item.get('duetInfo') or {}).get('duetFromId')
                post_type = 'quote' if duet_from_id and duet_from_id != '0' else 'original'

                try:
                    posted_at = datetime.fromtimestamp(int(item.get('createTime', 0)), tz=timezone.utc)
                except (ValueError, TypeError):
                    posted_at = datetime.now(tz=timezone.utc)

                stats = item.get('stats', {})

                post = Post(
                    platform='tiktok',
                    account_id=None,
                    posted_at=posted_at,
                    url=f"https://www.tiktok.com/@{username}/video/{video_id}",
                    content=item.get('desc'),
                    post_type=post_type,
                    likes=stats.get('diggCount', 0),
                    reposts=stats.get('shareCount', 0),
                    comments=stats.get('commentCount', 0),
                    platform_data=entry,
                )

                results.append((account, post))
            except json.JSONDecodeError:
                continue

    return results
