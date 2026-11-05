import re

HTML_TAG_PATTERN = re.compile(r'<[^>]*>')


def shorten_text(text: str, max_length: int) -> str:
    """Plain text version of text (HTML tags removed) cut to at most max_length characters at a word boundary."""
    plain_text = ' '.join(HTML_TAG_PATTERN.sub(' ', text).split())
    if len(plain_text) <= max_length:
        return plain_text
    return plain_text[:max_length].rsplit(' ', 1)[0]
