from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_on_this_page(self, locator):
        return len(self.driver.find_elements_by_css_selector(locator)) > 0

    def select_product_size(self):
        if self.is_on_this_page("td.options select"):
                element = self.driver.find_element_by_css_selector("td.options select")
                Select(element).select_by_index(1)
    @property
    def quantity_input(self):
        return self.driver.find_element_by_css_selector("div.buy_now input[name='quantity']")

    @property
    def add_to_cart_button(self):
        return self.driver.find_element_by_css_selector("div.buy_now button")
