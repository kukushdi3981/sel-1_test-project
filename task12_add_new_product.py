import pytest
import os
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
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("div#box-apps-menu-wrapper"))
    driver.find_element_by_css_selector("div#box-apps-menu-wrapper a[href$=catalog]").click()

#   проверяем появления заголовка страницы после нажатия
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("h1"))

    driver.find_element_by_css_selector("div a[href$=edit_product]").click()

def Create_new_product(driver, dict):
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("h1"))

#   заполняем вкладку General
    driver.find_element_by_css_selector("div#tab-general label input[value='1']").click()
    driver.find_element_by_css_selector("div#tab-general input[name='name[en]']").send_keys(dict['ProdName'])
    driver.find_element_by_css_selector("div#tab-general input[name='code']").send_keys(dict['ProdCode'])
    driver.find_element_by_css_selector("div#tab-general input[name='quantity']").clear()
    driver.find_element_by_css_selector("div#tab-general input[name='quantity']").send_keys(dict['Quantity'])

    element = driver.find_element_by_css_selector("div#tab-general select[name='quantity_unit_id']")
    Select(element).select_by_visible_text("pcs")

    driver.find_element_by_css_selector("div#tab-general input[name='new_images[]']").send_keys(dict['ImagePath'])

#   переходим на вкладку Information
    driver.find_element_by_css_selector("div.tabs a[href$=information]").click()

    WebDriverWait(driver, 5).until(lambda driver : \
                                       driver.find_element_by_css_selector("div#tab-information select[name='manufacturer_id']"))

#   заполняем вкладку Information
    element = driver.find_element_by_css_selector("div#tab-information select[name='manufacturer_id']")
    Select(element).select_by_index(1)

    driver.find_element_by_css_selector("div#tab-information input[name='short_description[en]']").send_keys(dict['ShortDescr'])
    driver.find_element_by_css_selector("div#tab-information div.trumbowyg-editor").send_keys(dict['Description'])
    driver.find_element_by_css_selector("div#tab-information input[name='head_title[en]']").send_keys(dict['HeadTitle'])

#   переходим на вкладку Prices
    driver.find_element_by_css_selector("div.tabs a[href$=prices]").click()

    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("div#tab-prices h2:first-child"))

#   заполняем вкладку Prices
    driver.find_element_by_css_selector("div#tab-prices input[name='purchase_price']").clear()
    driver.find_element_by_css_selector("div#tab-prices input[name='purchase_price']").send_keys(dict['PurchasePrice'])

    element = driver.find_element_by_css_selector("div#tab-prices select[name='purchase_price_currency_code']")
    Select(element).select_by_value("USD")

    driver.find_element_by_css_selector("div#tab-prices input[name='prices[USD]']").clear()
    driver.find_element_by_css_selector("div#tab-prices input[name='prices[USD]']").send_keys(dict['PriceUSD'])

#   Сохраняем созданный товар
    driver.find_element_by_css_selector("span.button-set button[name='save']").click()

    prod_link = driver.find_element_by_link_text(dict['ProdName'])
    print(prod_link.text)

    assert "My product 1" == prod_link.text


def test_Add_new_product(driver):
    product_info = {
        "ProdName": "My product 1",
        "ProdCode": "p0001",
        "Quantity": "21",
        "ImagePath": "",
        "ShortDescr": "description",
        "Description": "full description",
        "HeadTitle": "First product",
        "PurchasePrice": "12",
        "PriceUSD" : "18"
    }

    os.chdir(os.path.dirname(__file__))
    product_info['ImagePath'] = os.getcwd() + "\\no_image.png"

    driver.get('http://localhost/litecart/admin/')
    login(driver, "admin", "admin")
    Open_add_new_product_page(driver)
    Create_new_product(driver, product_info)
    logout(driver)
