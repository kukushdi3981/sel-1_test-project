import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import time


@pytest.fixture
def driver(request):
#    wd = webdriver.Chrome()  # Optional argument, if not specified will search path.
    wd = webdriver.Remote("http://192.168.56.1:4444/wd/hub", desired_capabilities={"browserName": "chrome", "platform": "VISTA"})
#    wd = webdriver.Remote("http://192.168.1.41:4444/wd/hub", desired_capabilities={"browserName": "internet explorer", "platform": "VISTA"})
    print(wd.capabilities)
#    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


def login(driver, username, password):
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

def logout(driver):
    WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_css_selector("div.header"))

    driver.find_element_by_css_selector("a[title='Logout']").click()

def Open_add_new_product_page(driver):
    WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_css_selector("div#box-apps-menu-wrapper"))
    driver.find_element_by_css_selector("div#box-apps-menu-wrapper a[href$=catalog]").click()

#   проверяем появления заголовка страницы после нажатия
    WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_css_selector("h1"))

    driver.find_element_by_css_selector("div a[href$=edit_product]").click()

def test_selenium_grid(driver):
    driver.get('http://192.168.1.41/litecart/admin/')
    login(driver, "admin", "admin")
    Open_add_new_product_page(driver)
    logout(driver)
