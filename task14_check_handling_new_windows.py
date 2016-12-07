import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()  # Optional argument, if not specified will search path.
#    wd = webdriver.Ie()
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

def open_add_new_country_page(driver):
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("div#box-apps-menu-wrapper"))
    driver.find_element_by_css_selector("div#box-apps-menu-wrapper a[href$=countries]").click()

#   проверяем появления заголовка страницы после нажатия
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("h1"))
    driver.find_element_by_css_selector("#content a.button").click()

def open_and_close_new_windows(webdriver, element):
    wait = WebDriverWait(webdriver, 10)
    # запоминаем идентификатор текущего окна
    main_window = webdriver.current_window_handle
    # запоминаем идентификатор уже открытых окон
    exist_windows = webdriver.window_handles
    # открывает новое окно
    element.click()
    # ожидание появления нового окна,
    # идентификатор которого отсутствует в списке exist_windows
    wait.until(lambda webdriver: len(exist_windows) != len(webdriver.window_handles))

    handles = webdriver.window_handles
    handles.remove(main_window)

    # переключаемся в новое окно
    webdriver.switch_to_window(handles[0])
#    webdriver.switch_to_window(webdriver.window_handles[-1])
    # ожидаем загрузки стрницы в новом окне
    wait.until(lambda webdriver : webdriver.find_element_by_css_selector("h1"))
    webdriver.close()

    # возвращаемся в исходное окно
    webdriver.switch_to_window(main_window)

def click_links_to_open_windows(driver):
    WebDriverWait(driver, 5).until(lambda driver : driver.find_element_by_css_selector("td#content"))

    links = driver.find_elements_by_css_selector("form a[target='_blank']")

    for link in links:
        open_and_close_new_windows(driver, link)

    driver.find_element_by_css_selector("span.button-set button[name='cancel']").click()

def test_check_handle_new_windows(driver):
    driver.get('http://localhost/litecart/admin/')
    login(driver, "admin", "admin")
    open_add_new_country_page(driver)
    click_links_to_open_windows(driver)
    logout(driver)
