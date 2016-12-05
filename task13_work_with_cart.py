import pytest
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


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


def get_random_product(webdriver, locator):
    if check_exists_by_locator(webdriver, locator):
        el_products = webdriver.find_elements_by_css_selector(locator)
        element = el_products[random.randint(0,len(el_products))-1]
    else:
        element = None
    return element


def add_product_to_cart(driver, text):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "box-most-popular")))

#   ищем продукты и берем произвольный продукт для добавления в корзину
    product = get_random_product(driver, "div#box-most-popular div.content a.link")
    if product != None:
        product.click()

#       ожидаем перехода на страницу выбранного продукта
        wait.until(EC.presence_of_element_located((By.ID, "box-product")))

        if check_exists_by_locator(driver, "td.options select"):
                element = driver.find_element_by_css_selector("td.options select")
                Select(element).select_by_index(1)

        driver.find_element_by_css_selector("div.buy_now input[name='quantity']").clear()
        driver.find_element_by_css_selector("div.buy_now input[name='quantity']").send_keys("1")
        driver.find_element_by_css_selector("div.buy_now button").click()

#       ожидаем помещения текста в корзину (увеличения количества товаров в корзине на 1)
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'div#cart span.quantity'), text))

def open_cart(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-most-popular")))
    driver.find_element_by_css_selector("div#cart a.link").click()

def delete_products_from_cart(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "checkout-summary-wrapper")))

#   определяем количество товаров для удаления из корзины (кол-во строк в таблице)
    rows = driver.find_elements_by_css_selector("div#checkout-summary-wrapper td.item")

    for i in range(len(rows)):
#       определяем элемент исчезновение которого будем ожидать после очередного удаления товара из корзины
        if i != len(rows)-1:
            shortcuts = driver.find_elements_by_css_selector("li.shortcut a")
            shortcuts[0].click()
        else:
            shortcuts = driver.find_elements_by_css_selector("li.item a[class='image-wrapper shadow']")

        products = driver.find_elements_by_css_selector("li.item button[name='remove_cart_item']")
        products[0].click()

#       ожидаем исчезновение нужного элемента для продолжения действий
        wait.until(EC.staleness_of(shortcuts[0]))

#   ожидаем очистки корзины и переходим на главную страницу магазина
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#checkout-cart-wrapper a")))
    driver.find_element_by_css_selector("div#checkout-cart-wrapper a").click()


def test_work_with_cart(driver):
    driver.get('http://localhost/litecart/')
    for iter in range(3):
        add_product_to_cart(driver, str(iter+1))
        driver.back()
    open_cart(driver)
    delete_products_from_cart(driver)
