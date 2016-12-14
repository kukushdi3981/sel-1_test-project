import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(by, value)
    def after_find(self, by, value, driver):
        print(by, value, "found")
    def on_exception(self, exception, driver):
        print(exception)


@pytest.fixture
def driver(request):
#   включаем логирование браузера
    dc = DesiredCapabilities.CHROME
    dc['loggingPrefs'] = {'browser':'ALL'}
    wd = EventFiringWebDriver(webdriver.Chrome(desired_capabilities=dc), MyListener())

    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd


def login(driver, username, password):
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()

def logout(driver):
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("div.header"))

    driver.find_element_by_css_selector("a[title='Logout']").click()

def open_product_page(driver):
    count_error = 0
    wait = WebDriverWait(driver, 5)
    prod_elem = driver.find_elements_by_css_selector("tr.row a:nth-child(2)")

    for iter in range(1, len(prod_elem)):
        wait.until(lambda driver : driver.find_element_by_css_selector("table.dataTable"))

        prod_elem = driver.find_elements_by_css_selector("tr.row a:nth-child(2)")

        prod_elem[iter].click()
        # выводим в консоль лог браузера
        for entry in driver.get_log('browser'):
            print(entry)

            # проверяем лог браузера на ошибки
            if entry['level'] != 'INFO':
                count_error += count_error

        wait.until(lambda driver : driver.find_element_by_css_selector("div.tabs"))
        driver.back()

    if count_error > 0:
        print("В логе браузера присутствуют солобщения об ошибках. Продробности смотри в консоле вывода лога.")

    return count_error

def test_Check_br_log_on_products_page(driver):
    driver.get('http://localhost/litecart/admin/')
    login(driver, "admin", "admin")
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    err_cnt = open_product_page(driver)
    logout(driver)

    assert err_cnt == 0
