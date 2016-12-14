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

def check_exists_by_locator(driver, locator):
    return len(driver.find_elements_by_css_selector(locator)) > 0

def check_stickers(driver):
        dict = {}
        items = driver.find_elements_by_css_selector("div.content a.link")
        count = len(items)

        for i in range(count):
            l1 = len(items[i].find_elements_by_css_selector("div.content a.link div[title='New']"))
            l2= len(items[i].find_elements_by_css_selector("div.content a.link div[title='On Sale']"))
            if check_exists_by_locator(items[i], "div.content a.link div[title='New']") and l1 == 1:
                dict[i] = True
            elif check_exists_by_locator(items[i], "div.content a.link div[title='On Sale']") and l2 == 1:
                dict[i] = True
            else:
                dict[i] = False

        for key in dict:
            if dict[key] == False:
                result = False
            else:
                result = True

        if not result:
            print("Ошибка проверки, что у каждого товара имеется ровно один стикер")
        else:
            print("Проверка соответствия товара и стикера успешно прошла.")

        assert result == True


def test_example(driver):
    driver.get('http://localhost/litecart/')
    check_stickers(driver)
