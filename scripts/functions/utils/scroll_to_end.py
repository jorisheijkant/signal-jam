import random
import time


def scroll_to_end(driver, max_scrolls=5):
    scrolls_without_change = 0
    max_scrolls_without_change = 3
    previous_height = 0

    for scroll_count in range(max_scrolls):
        scroll_interval = random.randint(2, 5)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_interval)

        current_height = driver.execute_script("return document.body.scrollHeight")

        if current_height == previous_height:
            scrolls_without_change += 1
            print(f"Scroll {scroll_count + 1}: No change detected ({scrolls_without_change}/{max_scrolls_without_change})")

            if scrolls_without_change >= max_scrolls_without_change:
                print(f"Stopped scrolling after {scroll_count + 1} scrolls - no new content for {max_scrolls_without_change} consecutive scrolls")
                break
        else:
            scrolls_without_change = 0
            print(f"Scroll {scroll_count + 1}: Page height changed from {previous_height} to {current_height}")

        previous_height = current_height
    else:
        print(f"Completed maximum {max_scrolls} scrolls")
