import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/litecart/")
        self.wait.until(EC.presence_of_element_located((By.ID, "box-most-popular")))
        return self

    def is_on_this_page(self, locator):
        return len(self.driver.find_elements_by_css_selector(locator)) > 0

    def get_random_product(self, locator):
        if self.is_on_this_page(locator):
            el_products = self.driver.find_elements_by_css_selector(locator)
            element = el_products[random.randint(0,len(el_products))-1]
        else:
            element = None
        return element

    def select_product(self):
        product = self.get_random_product("div#box-most-popular div.content a.link")
        if product != None:
            product.click()

            #ожидаем перехода на страницу выбранного продукта
            self.wait.until(EC.presence_of_element_located((By.ID, "box-product")))
