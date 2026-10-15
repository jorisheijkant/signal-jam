import feedparser
from datetime import datetime, timezone


def fetch_rss_articles(source):
    feed = feedparser.parse(source["url"])
    language = feed.feed.get("language")
    return [_parse_entry(entry, source["name"], language) for entry in feed.entries]


def _parse_entry(entry, source_name, language):
    return {
        "url": entry.get("link"),
        "title": entry.get("title"),
        "source": source_name,
        "author": entry.get("author"),
        "language": language,
        "summary": entry.get("summary"),
        "content": _get_content(entry),
        "published_at": _get_published_at(entry),
    }


def _get_content(entry):
    if hasattr(entry, "content") and entry.content:
        return entry.content[0].get("value")
    return None


def _get_published_at(entry):
    time_struct = entry.get("published_parsed") or entry.get("updated_parsed")
    if time_struct:
        return datetime(*time_struct[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)
