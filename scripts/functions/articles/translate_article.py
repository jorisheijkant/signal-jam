import os
import time

from functions.articles.save_article_translation import save_article_translation
from functions.llm import translate_to_english
from functions.utils.shorten_text import shorten_text

TRANSLATED_CONTENT_LENGTH = 250


def get_languages_to_translate() -> list[str]:
    return os.getenv('TRANSLATE_ARTICLE_LANGUAGES', 'ru').split(',')


def translate_article(conn, llm, article: dict) -> bool:
    """Translate a stored article's title and the start of its content into English and save it onto its row.

    Only the first TRANSLATED_CONTENT_LENGTH characters of the content are translated, as plain text: it is a
    preview and keeps the local model fast.

    Needs the article's url, title, content and language. Returns whether it was translated: false when the
    language is not configured for translation or when the model failed, in which case the article stays as stored."""
    if article['language'] not in get_languages_to_translate():
        return False

    started_at = time.perf_counter()
    try:
        title_en = translate_to_english(llm, article['title'])
        content_preview = shorten_text(article['content'] or '', TRANSLATED_CONTENT_LENGTH)
        content_en = translate_to_english(llm, content_preview) if content_preview else None
    except Exception as error:
        print(f"  [translation failed] {article['url']} ({time.perf_counter() - started_at:.1f} seconds) — {error}")
        return False

    elapsed_seconds = time.perf_counter() - started_at
    save_article_translation(conn, article['url'], title_en, content_en)
    print(f"  [translated] {article['url']} ({elapsed_seconds:.1f} seconds)")
    return True
