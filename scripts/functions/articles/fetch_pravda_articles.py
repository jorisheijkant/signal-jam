import re
from datetime import datetime, timezone
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

_DATE_IN_URL = re.compile(r"/(\d{4})/(\d{2})/(\d{2})/")


def fetch_pravda_articles(browser, source):
    browser.get(source["url"])
    items = browser.find_elements(By.CLASS_NAME, source["news_item_element_class"])
    articles = [_parse_item(item, source["name"], source["language"]) for item in items]
    return _deduplicate_by_url([article for article in articles if article is not None])


def _deduplicate_by_url(articles):
    seen_urls = set()
    deduplicated = []
    for article in articles:
        if article["url"] not in seen_urls:
            seen_urls.add(article["url"])
            deduplicated.append(article)
    return deduplicated


def _parse_item(item, source_name, language):
    try:
        link = item.find_element(By.CLASS_NAME, "news-item__title")
    except NoSuchElementException:
        return None

    return {
        "url": link.get_attribute("href"),
        "title": link.get_attribute("textContent").strip(),
        "source": source_name,
        "author": None,
        "language": language,
        "summary": None,
        "content": None,
        "published_at": _get_published_at(item, link.get_attribute("href")),
    }


def _get_published_at(item, url):
    date_match = _DATE_IN_URL.search(url or "")
    if not date_match:
        return datetime.now(timezone.utc)

    year, month, day = (int(part) for part in date_match.groups())

    try:
        time_element = item.find_element(By.CLASS_NAME, "news-item__time")
        time_text = time_element.get_attribute("textContent").strip()
        hour, minute = (int(part) for part in time_text.split(":"))
    except (NoSuchElementException, ValueError):
        hour, minute = 0, 0

    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)
