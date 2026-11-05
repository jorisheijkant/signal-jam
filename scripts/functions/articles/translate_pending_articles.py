from functions.articles.build_translation_llm import build_translation_llm
from functions.articles.fetch_untranslated_articles import fetch_untranslated_articles
from functions.articles.translate_article import get_languages_to_translate, translate_article


def translate_pending_articles(conn, batch_size: int) -> int:
    """Translate up to batch_size stored articles that have no English title yet, returns the number translated.

    Relevant articles come first, then the newest."""
    llm = build_translation_llm()
    if llm is None:
        return 0

    articles = fetch_untranslated_articles(conn, get_languages_to_translate(), batch_size)
    print(f"Translating {len(articles)} articles")

    return sum(translate_article(conn, llm, article) for article in articles)
