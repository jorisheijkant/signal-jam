from trafilatura import extract


def scrape_article_content(browser, url):
    browser.get(url)
    return extract(browser.page_source)
