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
    wd = webdriver.Chrome()  # Optional argument, if not specified will search path.
    print(wd.capabilities)
#    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd


def login(driver, username, password):
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

def logout(driver):
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("div.header"))

    driver.find_element_by_css_selector("a[title='Logout']").click()

def Open_add_new_product_page(driver):
    driver.find_element_by_css_selector("div#box-apps-menu-wrapper a[href$=catalog]").click()

#   проверяем появления заголовка страницы после нажатия
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("h1"))

    driver.find_element_by_css_selector("div a[href$=edit_product]").click()

def Create_new_product(driver):
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("h1"))

#   заполняем вкладку General
    driver.find_element_by_css_selector("div#tab-general label input[value='1']").click()
    driver.find_element_by_css_selector("div#tab-general input[name='name[en]']").send_keys("My product 1")
    driver.find_element_by_css_selector("div#tab-general input[name='code']").send_keys("p0001")
    driver.find_element_by_css_selector("div#tab-general input[name='quantity']").clear()
    driver.find_element_by_css_selector("div#tab-general input[name='quantity']").send_keys(21)

    element = driver.find_element_by_css_selector("div#tab-general select[name='quantity_unit_id']")
    Select(element).select_by_visible_text("pcs")

    driver.find_element_by_css_selector("div#tab-general input[name='new_images[]']").send_keys("C:\\no_image.png")

#   переходим на вкладку Information
    driver.find_element_by_css_selector("div.tabs a[href$=information]").click()

    WebDriverWait(driver, 5).until(lambda driver : \
                                       driver.find_element_by_css_selector("div#tab-information select[name='manufacturer_id']"))

#   заполняем вкладку Information
    element = driver.find_element_by_css_selector("div#tab-information select[name='manufacturer_id']")
    Select(element).select_by_index(1)

    driver.find_element_by_css_selector("div#tab-information input[name='short_description[en]']").send_keys("description")
    driver.find_element_by_css_selector("div#tab-information div.trumbowyg-editor").send_keys("full description")
    driver.find_element_by_css_selector("div#tab-information input[name='head_title[en]']").send_keys("First product")

#   переходим на вкладку Prices
    driver.find_element_by_css_selector("div.tabs a[href$=prices]").click()

    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("div#tab-prices h2:first-child"))

#   заполняем вкладку Prices
    driver.find_element_by_css_selector("div#tab-prices input[name='purchase_price']").clear()
    driver.find_element_by_css_selector("div#tab-prices input[name='purchase_price']").send_keys("12")

    element = driver.find_element_by_css_selector("div#tab-prices select[name='purchase_price_currency_code']")
    Select(element).select_by_value("USD")

    driver.find_element_by_css_selector("div#tab-prices input[name='prices[USD]']").clear()
    driver.find_element_by_css_selector("div#tab-prices input[name='prices[USD]']").send_keys("18")

#   Сохраняем созданный товар
    driver.find_element_by_css_selector("span.button-set button[name='save']").click()

    prod_link = driver.find_element_by_link_text("My product 1")
    print(prod_link.text)

    assert "My product 1" == prod_link.text


def test_Add_new_product(driver):
    driver.get('http://localhost/litecart/admin/')
    login(driver, "admin", "admin")
    Open_add_new_product_page(driver)
    Create_new_product(driver)
    logout(driver)
