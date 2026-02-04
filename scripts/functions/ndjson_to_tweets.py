import json
from datetime import datetime

from classes import Account, Post

TWITTER_DATE_FORMAT = "%a %b %d %H:%M:%S %z %Y"


def ndjson_to_tweets(ndjson_path):
    results = []

    with open(ndjson_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            try:
                entry = json.loads(line)
                data = entry.get('data', {})
                core_data = data.get('core', {})
                legacy_data = data.get('legacy', {})

                tweet_id = data.get('rest_id') or data.get('id_str') or data.get('id')
                user_result = (core_data
                             .get('user_results', {})
                             .get('result', {}))
                user_core = user_result.get('core', {})
                handle = user_core.get('screen_name', '')
                display_name = user_core.get('name', '')

                if not tweet_id or not handle:
                    continue

                account = Account(
                    platform='twitter',
                    username=handle,
                    account_url=f"https://x.com/{handle}",
                    display_name=display_name.strip() or None,
                )

                in_reply_to = legacy_data.get('in_reply_to_screen_name')
                is_retweet = 'retweeted_status_result' in legacy_data

                if is_retweet:
                    post_type = 'repost'
                elif in_reply_to:
                    post_type = 'reply'
                else:
                    post_type = 'original'

                created_at_str = legacy_data.get('created_at', '')
                try:
                    posted_at = datetime.strptime(created_at_str, TWITTER_DATE_FORMAT)
                except (ValueError, TypeError):
                    posted_at = datetime.now()

                post = Post(
                    platform='twitter',
                    account_id=None,
                    posted_at=posted_at,
                    url=f"https://x.com/{handle}/status/{tweet_id}",
                    content=legacy_data.get('full_text') or legacy_data.get('text'),
                    post_type=post_type,
                    likes=legacy_data.get('favorite_count', 0),
                    reposts=legacy_data.get('retweet_count', 0),
                    comments=legacy_data.get('reply_count', 0),
                    platform_data=entry,
                )

                results.append((account, post))
            except json.JSONDecodeError:
                continue

    return results

