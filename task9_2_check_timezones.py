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

def check_exists_by_locator(driver, locator):
    return len(driver.find_elements_by_css_selector(locator)) > 0

def login(driver, username, password):
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

def check_countries(driver):
    countries = []
    diff = 0
    table = driver.find_element_by_css_selector("td#content")
    rows = table.find_elements_by_css_selector("tr.row a:not([title='Edit'])")
    count = len(rows)
    for i in range(count):
        countries.append(rows[i].get_attribute("innerText"))

    sort_list = sorted(countries)
    for j in range(count):
        if (countries[j] != sort_list[j]):
            diff += 1

    assert diff == 0

def check_timezones(driver):
    cur_timezones = []
    dict = {}

    table = driver.find_element_by_css_selector("table.dataTable")
    rows = table.find_elements_by_css_selector("tr.row a:not([title='Edit'])")

    for iteration in range(len(rows)):
        diff = 0
        cur_timezones = []

        if iteration > 0:
            driver.back()
            rows = driver.find_elements_by_css_selector("table.dataTable tr.row a:not([title='Edit'])")

        rows[iteration].click()

#      проверяем появления заголовка страницы после нажатия
        WebDriverWait(driver, 5).until(lambda webdriver : webdriver.find_element_by_css_selector("h1"))

        el_timezones = driver.find_elements_by_css_selector("table.dataTable select:not(.select2-hidden-accessible)")
        for i in range(len(el_timezones)):
            select_timezone = el_timezones[i].find_element_by_css_selector("option[selected='selected']")
            cur_timezones.append(select_timezone.text)

        sort_list = sorted(cur_timezones)
        for j in range(len(cur_timezones)):
            if (cur_timezones[j] != sort_list[j]):
                diff += 1

        dict['coutry'+ str(iteration+1)] = diff

#      проверяем, что значения timezone для всех стан отсортированы в алфавитном порядке
    for key in dict:
        if dict[key] == 0:
            result = True
        else:
            result = False
            print("Ошибка расположения временных зон для страны" + str(key))

    assert result == True


def logout(driver):
    driver.find_element_by_xpath("//*[@title='Logout']").click()

def test_example(driver):
    driver.get('http://localhost/litecart/admin/')
    login(driver, "admin", "admin")
    driver.get('http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones')
    check_timezones(driver)
    logout(driver)

