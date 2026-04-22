import re
from urllib.parse import urlparse


def twitter_handle_from_account_url(twitter_account_url):
    if not twitter_account_url:
        return None

    url = str(twitter_account_url).strip()

    if not url:
        return None

    if url.startswith('@'):
        handle = url[1:].strip()
        return handle if handle else None

    if 'twitter.com' in url.lower() or 'x.com' in url.lower():
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            parsed = urlparse(url)
            path = parsed.path.strip('/')

            if path:
                handle = path.split('/')[0]
                handle = handle.split('?')[0].split('#')[0]
                return handle if handle else None
        except Exception:
            pass

    handle = url.lstrip('@').strip('/')
    handle = re.sub(r'[^a-zA-Z0-9_]', '', handle)

    return handle if handle else None
