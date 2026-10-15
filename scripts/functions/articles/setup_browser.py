import os
import shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

SCRAPING_TOOLS_DIR = Path(__file__).parent.parent.parent / "scraping_tools"


def setup_browser():
    options = Options()
    options.add_argument("-headless")
    _configure_dns_over_https(options)
    geckodriver_path = shutil.which("geckodriver") or str(SCRAPING_TOOLS_DIR / "geckodriver")
    return webdriver.Firefox(service=Service(geckodriver_path), options=options)


def _configure_dns_over_https(options):
    doh_url = os.getenv("DNS_OVER_HTTPS_URL")
    if not doh_url:
        return
    options.set_preference("network.trr.mode", 3)
    options.set_preference("network.trr.uri", doh_url)
