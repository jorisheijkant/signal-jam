import re
import time
import os

from functions.utils.name_to_slug import name_to_slug
from functions.utils.copy_last_ndjson import copy_last_ndjson
from functions.utils.scroll_to_end import scroll_to_end

def scrape_term(driver, term_url, term):
    term_folder_friendly = name_to_slug(term)
    output_folder = f"data/{term_folder_friendly}"
    os.makedirs(output_folder, exist_ok=True)

    handles = driver.window_handles

    driver.switch_to.window(handles[0])
    driver.execute_script("document.querySelector('button.reset-all').click();")
    driver.switch_to.new_window("tab")

    driver.get(term_url)

    scroll_to_end(driver)

    driver.switch_to.window(handles[0])
    time.sleep(5)
    num_items = int(re.sub("[^0-9]", "", driver.execute_script(
        f"return document.querySelector('#stats-twittercom .num-items').innerText")))
    print(f"Found {num_items} for term {term}")

    if num_items > 0:
        driver.execute_script("document.querySelector('#stats-twittercom .download-ndjson').click();")
        filename = copy_last_ndjson(output_folder, term_folder_friendly)
        return filename
    else: 
        return None
