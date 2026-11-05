from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.articles import (
    fetch_pravda_articles,
    find_existing_urls,
    insert_article,
    load_json_file,
    matches_article_filter_terms,
    scrape_article_content,
    setup_browser,
)

SOURCES_PATH = Path(__file__).parent / 'source_data' / 'articles' / 'pravda_sources.json'
FILTER_TERMS_PATH = Path(__file__).parent / 'source_data' / 'articles' / 'search_terms.json'


def main():
    sources = load_json_file(SOURCES_PATH)
    filter_terms = load_json_file(FILTER_TERMS_PATH)
    conn = Database().conn
    browser = setup_browser()

    for source in sources:
        articles = fetch_pravda_articles(browser, source)
        existing_urls = find_existing_urls(conn, [article['url'] for article in articles])
        new_articles = [article for article in articles if article['url'] not in existing_urls]

        for article in new_articles:
            article['content'] = scrape_article_content(browser, article['url'])
            article['relevant_for_signal_jam_theme'] = matches_article_filter_terms(article, filter_terms)
            insert_article(conn, article)

        print(f"{source['name']}: {len(new_articles)}/{len(articles)} new articles saved")

    browser.quit()
    conn.close()


if __name__ == '__main__':
    main()
