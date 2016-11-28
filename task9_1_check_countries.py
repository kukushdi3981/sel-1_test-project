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

def get_countries_rows(driver, locator):
    table = driver.find_element_by_css_selector("td#content")
    country_rows = table.find_elements_by_css_selector(locator)
    return country_rows

def check_countries_sorted(driver):
    countries = []
    diff = 0
    rows = get_countries_rows(driver, "tr.row a:not([title='Edit'])")
    count = len(rows)
    for i in range(count):
        countries.append(rows[i].get_attribute("innerText"))

    sort_list = sorted(countries)
    for j in range(count):
        if (countries[j] != sort_list[j]):
            diff += 1

    assert diff == 0

def check_country_timezones_sorted(driver):
    dict = {}
    found = 0

    rows = get_countries_rows(driver, "tr.row")

    for irw in range(len(rows)):
        if found > 0:
            driver.back()
            rows = get_countries_rows(driver, "tr.row")
            found = 0

#       получаем ячейки строки со страной и получаем ссылку на стану и число timezones для нее
        cells = rows[irw].find_elements_by_tag_name("td")
        cnt_link = cells[4].find_element_by_css_selector("a")
        cnt_name = cells[4].text
        cnt_timezones =cells[5].text

#       для страны с timezones>0, открываем эту страну и получаем список ее timezones
        if int(cnt_timezones) > 0:
            lst_timezones = []
            diff = 0
            found +=1
            cnt_link.click()

            tz_rows = driver.find_elements_by_css_selector("table.dataTable tr:not(.header)")

            for i in range(len(tz_rows)-1):
                tz_cells =tz_rows[i].find_elements_by_tag_name("td")
                timezone =tz_cells[2].text
                lst_timezones.append(timezone)

            sort_list = sorted(lst_timezones)
            for j in range(len(lst_timezones)):
                if (lst_timezones[j] != sort_list[j]):
                    diff += 1

            dict[cnt_name] = diff

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

def test_check_task91(driver):
    driver.get('http://localhost/litecart/admin/')
    login(driver, "admin", "admin")
    driver.get('http://localhost/litecart/admin/?app=countries&doc=countries')
    check_countries_sorted(driver)
    check_country_timezones_sorted(driver)
    logout(driver)

