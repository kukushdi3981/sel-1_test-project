import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_example():
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get('http://www.google.com/')
    time.sleep(1) # Let the user actually see something!
    search_box = driver.find_element_by_name('q')
    search_box.send_keys('ChromeDriver')
    search_box.submit()
    driver.quit()

test_example()
