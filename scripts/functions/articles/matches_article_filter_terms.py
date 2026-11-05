from functions.utils.matches_filter_terms import matches_filter_terms


def matches_article_filter_terms(article: dict, filter_terms: list[str]) -> bool:
    """True if the title, summary or content of the article contains any filter term."""
    searchable_text = ' '.join(article.get(field) or '' for field in ('title', 'summary', 'content'))
    return matches_filter_terms(searchable_text, filter_terms)
