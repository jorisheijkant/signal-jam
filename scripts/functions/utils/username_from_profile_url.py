from urllib.parse import urlparse

from functions.utils.twitter_handle_from_account_url import twitter_handle_from_account_url


def username_from_profile_url(platform, profile_url):
    if platform == 'twitter':
        return twitter_handle_from_account_url(profile_url)

    first_path_segment = urlparse(profile_url.strip()).path.strip('/').split('/')[0]
    return first_path_segment.lstrip('@') or None
