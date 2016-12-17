from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BlockCartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_adding_prod_to_cart(self, text):
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'div#cart span.quantity'), text))

    @property
    def cart_link_button(self):
        return self.driver.find_element_by_css_selector("div#cart a.link")
