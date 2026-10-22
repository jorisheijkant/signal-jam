def matches_filter_terms(content: str | None, filter_terms: list[str] | None) -> bool:
    """True if the content contains any filter term. Without filter terms every post counts as a match."""
    if not filter_terms:
        return True

    lowered_content = (content or '').lower()
    return any(term.lower() in lowered_content for term in filter_terms)
