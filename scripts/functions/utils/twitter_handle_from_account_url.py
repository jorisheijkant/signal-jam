import re
from urllib.parse import urlparse

def twitter_handle_from_account_url(twitter_account_url):
    """
    Extract Twitter/X handle from various URL formats.

    Handles:
    - https://twitter.com/username
    - https://x.com/username
    - https://www.twitter.com/username
    - twitter.com/username
    - @username
    - username (direct handle)
    - URLs with trailing slashes, query parameters, etc.

    Returns:
    - Clean handle without @ symbol
    - None if invalid or empty input
    """
    # Handle None or empty input
    if not twitter_account_url:
        return None

    # Convert to string and strip whitespace
    url = str(twitter_account_url).strip()

    if not url:
        return None

    # If it starts with @, just remove it
    if url.startswith('@'):
        handle = url[1:].strip()
        return handle if handle else None

    # If it looks like a URL, parse it
    if 'twitter.com' in url.lower() or 'x.com' in url.lower():
        # Add https:// if missing protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            # Parse the URL
            parsed = urlparse(url)

            # Get the path and remove leading/trailing slashes
            path = parsed.path.strip('/')

            # Split by slash and get the first part (handle)
            # This handles URLs like twitter.com/username/status/123456
            if path:
                handle = path.split('/')[0]

                # Remove query parameters if they somehow got through
                handle = handle.split('?')[0].split('#')[0]

                return handle if handle else None
        except Exception:
            # If URL parsing fails, fall through to direct return
            pass

    # If it doesn't look like a URL, assume it's already a handle
    # Remove any @ symbols, slashes, or other unwanted characters
    handle = url.lstrip('@').strip('/')

    # Basic validation: Twitter handles are alphanumeric + underscore, 1-15 chars
    # But we'll be lenient and just remove obviously invalid characters
    handle = re.sub(r'[^a-zA-Z0-9_]', '', handle)

    return handle if handle else None

