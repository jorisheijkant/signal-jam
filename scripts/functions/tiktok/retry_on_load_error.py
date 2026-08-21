import random
import time

from selenium.webdriver.common.by import By

MAX_REFRESH_ATTEMPTS = 3
MIN_REFRESH_WAIT_SECONDS = 2
MAX_REFRESH_WAIT_SECONDS = 6

ERROR_MESSAGE_XPATH = "//*[contains(text(), 'Something went wrong')]"
REFRESH_BUTTON_XPATH = "//button[contains(., 'Refresh')]"


def retry_on_load_error(driver):
    """Click TikTok's 'Refresh' button when a 'Something went wrong' error card appears.

    TikTok occasionally fails to load more posts mid-scroll and shows this error
    card instead. Retries up to MAX_REFRESH_ATTEMPTS times with a randomized pause
    between clicks, then gives up so the caller can move on to the next account.
    """
    for attempt in range(1, MAX_REFRESH_ATTEMPTS + 1):
        if not driver.find_elements(By.XPATH, ERROR_MESSAGE_XPATH):
            return

        refresh_buttons = driver.find_elements(By.XPATH, REFRESH_BUTTON_XPATH)
        if not refresh_buttons:
            return

        print(f"  'Something went wrong' detected, clicking Refresh (attempt {attempt}/{MAX_REFRESH_ATTEMPTS})")
        driver.execute_script("arguments[0].click();", refresh_buttons[0])
        time.sleep(random.uniform(MIN_REFRESH_WAIT_SECONDS, MAX_REFRESH_WAIT_SECONDS))
