import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()  # Optional argument, if not specified will search path.
#    wd = webdriver.Ie()

    print(wd.capabilities)
#    wd.implicitly_wait(1)
    request.addfinalizer(wd.quit)
    return wd

def check_value(cur_val, expect_val):
    if cur_val == expect_val:
        return True
    else:
        return False

def compare_dicts(dict1, dict2):
    for key in dict1:
        if dict1[key] == dict2[key]:
            result = True
        else:
            result = False
            print("Не совпало значение с ожидаемым для свойства '" + key + "'")

    return result

def check_dict(dict):
    for key in dict:
        if dict[key] == True:
            result = True
        else:
            result = False
            print("Не прошло проверку атрибут стиля '" + key + "'")
    return result

def check_style_by_attribute(webdriver, locator, atr_value):
    attr = webdriver.find_element_by_css_selector(locator).get_attribute("class")
    if attr == atr_value:
        return True
    else:
        return False


def get_el_product(webdriver, locator):
    element = webdriver.find_elements_by_css_selector(locator)
    return element[0]

def check_product_prop_and_styles(driver):
    dict_product_lst_props = {}
    dict_product_props = {}
    dict_el_style = {}

#   получение свойств и стилей продукта на главной странице
    product = get_el_product(driver, "div#box-campaigns a.link")
    dict_product_lst_props["prod_title"] = product.get_attribute("title")

    reg_pr_element = product.find_element_by_css_selector("s.regular-price")
    dict_product_lst_props["reg_price"] = reg_pr_element.get_attribute("textContent")
    lst_reg_pr_color = reg_pr_element.value_of_css_property("color")

    camp_pr_element = product.find_element_by_css_selector("strong.campaign-price")
    dict_product_lst_props["campaign_price"] = camp_pr_element.get_attribute("textContent")
    lst_camp_pr_color = camp_pr_element.value_of_css_property("color")

#   проверяем стиль цены на первой страницы
    dict_el_style["lst_s"] = check_style_by_attribute(product, "s", "regular-price")
    dict_el_style["lst_strong"] = check_style_by_attribute(product, "strong", "campaign-price")

    product.click()
#   проверяем появления заголовка страницы продукта
    WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_css_selector("div#box-product h1.title"))

#   получение свойств и стилей продукта на странице выбранного продукта
    sel_product = get_el_product(driver, "div#box-product h1.title")
    dict_product_props["prod_title"] = sel_product.get_attribute("textContent")

    sel_reg_pr_element = get_el_product(driver,"div.content s.regular-price")
    dict_product_props["reg_price"] = sel_reg_pr_element.get_attribute("textContent")
    reg_pr_color = sel_reg_pr_element.value_of_css_property("color")

    sel_camp_pr_element = get_el_product(driver,"div.content strong.campaign-price")
    dict_product_props["campaign_price"] = sel_camp_pr_element.get_attribute("textContent")
    camp_pr_color = sel_camp_pr_element.value_of_css_property("color")

#   проверяем стиль цены на второй странице товара
    dict_el_style["pr_s"] = check_style_by_attribute(driver, "div.content s", "regular-price")
    dict_el_style["pr_strong"] = check_style_by_attribute(driver, "div.price-wrapper strong", "campaign-price")

#   проверяем совпадение цвета цены скидки
    dict_el_style["color"] = check_value(lst_camp_pr_color, camp_pr_color)

#   driver.back()

#   проверяем совпадение атрибутов товара и стилей товара на 2-х страницах
    prop_result = compare_dicts(dict_product_lst_props, dict_product_props)
    style_res = check_dict(dict_el_style)

    assert prop_result == True
    assert style_res == True

def test_example(driver):
    driver.get('http://localhost/litecart/')
    check_product_prop_and_styles(driver)
