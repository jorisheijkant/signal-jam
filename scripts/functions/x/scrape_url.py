import re
import time
import os
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from functions.utils.name_to_slug import name_to_slug
from functions.utils.copy_last_ndjson import copy_last_ndjson
from functions.utils.scroll_to_end import scroll_to_end

SCRIPTS_DIR = Path(__file__).parent.parent.parent
DATA_DIR = SCRIPTS_DIR.parent / "data"


def scrape_url(driver, url, label):
    label_slug = name_to_slug(label)
    output_folder = DATA_DIR / label_slug
    os.makedirs(output_folder, exist_ok=True)

    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    driver.execute_script("document.querySelector('button.reset-all').click();")
    driver.switch_to.new_window("tab")

    try:
        driver.get(url)
    except TimeoutException:
        print(f"  [skipped] Navigation to {url} timed out, moving on")
        driver.close()
        driver.switch_to.window(handles[0])
        return None

    scroll_to_end(driver)

    driver.switch_to.window(handles[0])
    time.sleep(5)
    num_items = int(re.sub("[^0-9]", "", driver.execute_script(
        "return document.querySelector('#stats-twittercom .num-items').innerText")))
    print(f"Found {num_items} items for {label}")

    if num_items > 0:
        download_button = driver.find_element(
            By.CSS_SELECTOR, '#stats-twittercom .download-options button[data-format="ndjson"]')
        driver.execute_script("arguments[0].click();", download_button)
        return copy_last_ndjson(output_folder, label_slug)
    return None
