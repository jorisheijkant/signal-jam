from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

from db import Database
from functions.articles import (
    fetch_pravda_articles,
    find_existing_urls,
    insert_article,
    load_json_file,
    scrape_article_content,
    setup_browser,
)

SOURCES_PATH = Path(__file__).parent / 'source_data' / 'articles' / 'pravda_sources.json'


def main():
    sources = load_json_file(SOURCES_PATH)
    conn = Database().conn
    browser = setup_browser()

    for source in sources:
        articles = fetch_pravda_articles(browser, source)
        existing_urls = find_existing_urls(conn, [article['url'] for article in articles])
        new_articles = [article for article in articles if article['url'] not in existing_urls]

        for article in new_articles:
            article['content'] = scrape_article_content(browser, article['url'])
            insert_article(conn, article)

        print(f"{source['name']}: {len(new_articles)}/{len(articles)} new articles saved")

    browser.quit()
    conn.close()


if __name__ == '__main__':
    main()
