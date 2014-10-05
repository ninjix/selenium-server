#!/usr/bin/env python

from selenium import webdriver

browser = webdriver.Remote(
    command_executor='http://127.0.0.1:4444/wd/hub',
    desired_capabilities={
        'browserName': 'firefox'
        }
)
browser.get('http://python.org')
browser.save_screenshot('foo.png')
browser.quit()

