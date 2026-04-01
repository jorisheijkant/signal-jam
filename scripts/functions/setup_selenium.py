from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common import exceptions as selenium_exceptions
from selenium import webdriver

import os
import time
import shutil
from os.path import expanduser
from glob import glob
from platform import system
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SCRAPING_TOOLS_DIR = BASE_DIR / 'scraping_tools'

def get_profile():
    # Cloud deployment: point directly to a profile on a persistent volume
    profile_path = os.getenv('FIREFOX_PROFILE_PATH')
    if profile_path:
        print(f"Using profile from FIREFOX_PROFILE_PATH: {profile_path}")
        return profile_path

    profile_glob = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*",
    }.get(system(), "~/.mozilla/firefox/*")

    profiles = glob(expanduser(profile_glob))
    if len(profiles) == 0:
        print("No Firefox profile found. Make sure to first use Firefox and login to X/Twitter before launching this script.")
        exit(1)

    if len(profiles) > 1:
        print("Multiple profiles found:")
        profiles = sorted(profiles, key=lambda d: os.stat(d).st_mtime, reverse=True)
        for profile in profiles:
            mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(profile).st_mtime))
            print(f"- ({mtime}) {profile}")

        print("Choosing most recently used one (first in the list above)")
    else:
        print(f"Using profile {profiles[0]}")

    return profiles[0]

def copy_profile_to_local_folder(profile_dir):
    # When FIREFOX_PROFILE_PATH is set the profile is already in a writable
    # location on a persistent volume — no copy needed.
    if os.getenv('FIREFOX_PROFILE_PATH'):
        return Path(profile_dir)

    profile_file = SCRAPING_TOOLS_DIR / '.temp-profile'
    if profile_file.exists():
        print("Profile exists, overwriting the old one...")
        shutil.rmtree(profile_file)
    shutil.copytree(profile_dir, profile_file, ignore=lambda x, y: ["storage", "extensions", "signedInUser.json", "lock"])
    print(f"Copied profile {profile_dir} to local file {profile_file}")
    return profile_file

def setup_selenium():
    firefox_profile_directory = get_profile()
    local_profile_directory = copy_profile_to_local_folder(firefox_profile_directory)

    firefox_options = Options()
    firefox_options.add_argument("-headless")
    firefox_profile = webdriver.FirefoxProfile(str(local_profile_directory))
    firefox_profile.set_preference("security.fileuri.strict_origin_policy", False)
    firefox_profile.update_preferences()
    firefox_options.profile = firefox_profile

    # Use system geckodriver if available (cloud/Docker), otherwise fall back to local binary
    geckodriver_path = shutil.which('geckodriver') or str(SCRAPING_TOOLS_DIR / 'geckodriver')
    firefox_service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
    print(f"Opened Firefox")
    
    driver.install_addon(str(SCRAPING_TOOLS_DIR / 'zeeschuimer-v1.13.4.xpi'), temporary=True) # Change this if using a different version

    driver.execute_script((SCRAPING_TOOLS_DIR / 'stealth.js').read_text())
    print(f"Succesfully installed Zeeschuimer and loaded the stealth script...")

    # TODO: Tweak these for my specific use case
    driver.set_page_load_timeout(15) 
    driver.set_script_timeout(120)
    driver.implicitly_wait(5)

    driver.get("about:debugging#/runtime/this-firefox")
    time.sleep(0.1)

    # This gets the internal UUID of the extension to open it. 
    # N.B.: Watch your language setting here! Could be that you need to change it to text()="Internal UUID" 
    uuid = driver.find_element(By.XPATH, '//span[@title="Zeeschuimer"]//..//dt[text()="Internal UUID"]//..//dd').text
    zeeschuimer_url = f"moz-extension://{uuid}/popup/interface.html"
    driver.get(zeeschuimer_url)
    print(f"Zeeschuimer Extension screen loaded :)")

    # Reset all data in zeeschuimer and enable X/Twitter data collection
    # TODO: also toggle other platforms here (FB and Tiktok)
    time.sleep(2)
    driver.execute_script("document.querySelectorAll('.toggle-switch input').forEach((e) => { if(!e.checked) { e.click(); }}); ")

    driver.switch_to.window(driver.window_handles[0])

    return driver


