#!/usr/bin/env python
"""
Darwin box clock in and clock out automation
Steps:
    Make sure selenium is installed. Command to check
    1: python
    2: from selenium import webdriver

    If selenium is not installed, then installed it using
    1: sudo pip install selenium


    Set three (3) linux environment variables
    1: export mmt_username="<YOUR_USERNAME>
    2: export mmt_password="<YOUR_PASS>
    3: export chrome_driver_path="<CHROME_DRIVER_PATH>


    Now set a cron
    0: sudo chmod a+x /path/to/this/file.py
    1: crontab -e
    2: 0 11 23 * * * cd /path/to/this/file.py && ./clock_in_out.py
"""
import logging
import os
import subprocess

try:
    from selenium import webdriver
except ImportError:
    print("[ERROR] Selenium is not installed.")
    logging.error("[ERROR] Selenium is not installed.")
    print("[INFO] Installing...")
    logging.log("[INFO] Installing...", "")
    bash_command = "sudo pip install selenium"
    print("Enter your password...")
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    from selenium import webdriver

from selenium.webdriver.chrome.options import Options

user_name = os.getenv("mmt_username")
password = os.getenv("mmt_password")
chrome_driver_path = os.getenv("chrome_driver_path")
user_name_html_id = '//*[@id="userNameInput"]'
password_html_id = '//*[@id="passwordInput"]'
search_button_html_id = '//*[@id="submitButton"]'

logging.basicConfig(
    filename="/tmp/clock_in_out.log",
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def if_env_set_or_throw():
    if not all([chrome_driver_path, user_name, password]):
        msg = """Required environment variables not set. Please set following env. variables.\n\texport mmt_username="<YOUR_USERNAME>"
            \n\texport mmt_password="<YOUR_PASSWORD>"
            \n\texport chrome_driver_path="<CHROME_DRIVER_PATH>"
        """
        logging.error(msg)
        raise Exception(msg)


def clock_in_or_out():
    chr_options = get_chrome_options()

    driver = webdriver.Chrome(chrome_driver_path, options=chr_options)
    driver.get("https://gommt.darwinbox.in")

    # Filling username
    user_name_field = driver.find_element_by_xpath(user_name_html_id)
    user_name_field.send_keys(user_name)

    # Filling password
    password_field = driver.find_element_by_xpath(password_html_id)
    password_field.send_keys(password)

    # Clicking on login button
    login_button = driver.find_element_by_xpath(search_button_html_id)
    login_button.click()

    # Not working, so using plain JS in code
    # clock_out_button = driver.find_element_by_xpath(clock_out_html_id)
    # clock_out_button.click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, clock_out_html_id))).click()

    # Working code
    action = driver.execute_script("return document.getElementsByClassName('tool_tip_btn')[0].innerText")
    action_log = "[INFO] Doing %s" % action
    print(action_log)
    logging.info(action_log)
    driver.execute_script("document.getElementById('attendance-logger-widget').click()")
    driver.execute_script("document.getElementsByClassName('submit_clockInOut')[0].click()")


def get_chrome_options():
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    chr_options.add_argument("start-maximized")
    chr_options.add_argument("disable-infobars")
    chr_options.add_argument("--disable-extensions")
    chr_options.add_argument('--headless')
    chr_options.add_argument('--no-sandbox')
    chr_options.add_argument('--disable-dev-shm-usage')
    chr_options.add_argument('--window-size=1920x1480')
    return chr_options


if __name__ == '__main__':
    if_env_set_or_throw()
    clock_in_or_out()
