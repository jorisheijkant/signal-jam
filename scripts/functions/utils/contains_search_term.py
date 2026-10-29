import json
import re
import unicodedata
from urllib.parse import unquote

SCHEME_PATTERN = re.compile(r'^https?://')


def fold_accents(text: str) -> str:
    return ''.join(
        character for character in unicodedata.normalize('NFKD', text)
        if not unicodedata.combining(character)
    )


def split_search_term_into_words(search_term: str) -> list[str]:
    """Decode a URL-encoded search term and strip quotes and URL scheme, so '%22https://rt.com%22' becomes ['rt.com']."""
    decoded_term = unquote(search_term).strip().strip('"')
    unschemed_term = SCHEME_PATTERN.sub('', decoded_term)
    return fold_accents(unschemed_term).lower().split()


def contains_search_term(post, search_term: str) -> bool:
    """True if every word of the search term appears in the post's text or in its data (which holds expanded link URLs).

    Platforms match multi-word searches on the words in any order, so the exact phrase is not required.
    Only the 'data' part of the capture is searched: the rest is Zeeschuimer metadata that includes the search URL itself."""
    post_data = (post.platform_data or {}).get('data', {})
    searchable_text = fold_accents(f"{post.content or ''} {json.dumps(post_data, ensure_ascii=False)}").lower()

    # The lookbehind keeps 'rt.com' from matching inside 'smart.com'
    return all(
        re.search(rf'(?<![\w-]){re.escape(word)}', searchable_text)
        for word in split_search_term_into_words(search_term)
    )
