import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()  # Optional argument, if not specified will search path.
    print(wd.capabilities)
    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

def login(driver, username, password):
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

def logout(driver):
    driver.find_element_by_xpath("//*[@title='Logout']").click()

def test_example(driver):
    driver.get('http://localhost/litecart/admin/')
    login(driver, "admin", "admin")
    logout(driver)

