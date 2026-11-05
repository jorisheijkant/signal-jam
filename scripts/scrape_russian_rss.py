import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.articles import (
    build_translation_llm,
    fetch_rss_articles,
    find_existing_urls,
    insert_article,
    load_json_file,
    matches_article_filter_terms,
    scrape_article_content,
    setup_browser,
    translate_article,
)
from functions.utils.configure_dns_resolver import configure_dns_resolver

FEEDS_PATH = Path(__file__).parent / 'source_data' / 'articles' / 'russian_feeds.json'
FILTER_TERMS_PATH = Path(__file__).parent / 'source_data' / 'articles' / 'search_terms.json'


def main():
    configure_dns_resolver(os.getenv('DNS_RESOLVER'))
    sources = load_json_file(FEEDS_PATH)
    filter_terms = load_json_file(FILTER_TERMS_PATH)
    conn = Database().conn
    browser = setup_browser()
    translation_llm = build_translation_llm()

    for source in sources:
        articles = fetch_rss_articles(source)
        existing_urls = find_existing_urls(conn, [article['url'] for article in articles])
        new_articles = [article for article in articles if article['url'] not in existing_urls]

        for article in new_articles:
            article['content'] = scrape_article_content(browser, article['url'])
            article['relevant_for_signal_jam_theme'] = matches_article_filter_terms(article, filter_terms)
            insert_article(conn, article)
            if translation_llm:
                translate_article(conn, translation_llm, article)

        print(f"{source['name']}: {len(new_articles)}/{len(articles)} new articles saved")

    browser.quit()
    conn.close()


if __name__ == '__main__':
    main()
