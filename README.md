# Darwin box clock in and clock out automation
---
## Steps:
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
