import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()  # Optional argument, if not specified will search path.
    print(wd.capabilities)
#    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

def check_exists_by_locator(driver, locator):
    return len(driver.find_elements_by_css_selector(locator)) > 0

def login(driver, username, password):
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

def logout(driver):
    driver.find_element_by_css_selector("a[title='Logout']").click()

def menu_clicker(driver):
#  ищем все элементы меню верхнего уровня
    menu_items = driver.find_elements_by_css_selector("div#box-apps-menu-wrapper a")
    cols = len(menu_items)

    for iteration in range(cols):
        colsub = 0
        i = 1

        if iteration == 0:
            item = menu_items[iteration]
        else:
#           для последующих итераций ищем следующий элемент верхнего уровня, следующий за выбранным
            item = driver.find_element_by_css_selector("li#app-.selected + li a")

        item.click()

#      проверяем появления заголовка страницы после нажатия
        WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("h1"))

        if check_exists_by_locator(driver, "ul.docs"):
            element = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_css_selector("ul.docs"))

#           определяем количество вложенных пунктов подменю в активном пункте меню
            menu_subitems = element.find_elements_by_css_selector("a")
            colsub = len(menu_subitems)

#       прокликиваем каждый пункт подменю(кроме первого, который автоматически открыт при клике на пункте меню верхнего уровня)
#       и проверяем появления заголовка
        while i>=1 and i<=colsub:
            if i>1:
                WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("h1"))
                menu_subitems = driver.find_elements_by_css_selector("ul.docs a")
                menu_subitems[i-1].click()
            i+=1


def test_example(driver):
    driver.get('http://localhost/litecart/admin/')
    login(driver, "admin", "admin")
    menu_clicker(driver)
    logout(driver)

