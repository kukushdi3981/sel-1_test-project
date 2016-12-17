from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def del_from_cart_button(self):
        return self.driver.find_elements_by_css_selector("li.item button[name='remove_cart_item']")

    @property
    def smal_prod_icons(self):
        return self.driver.find_elements_by_css_selector("li.shortcut a")

    @property
    def product_image(self):
        return self.driver.find_elements_by_css_selector("li.item a[class='image-wrapper shadow']")

    @property
    def back_main_page_link(self):
        return self.driver.find_element_by_css_selector("div#checkout-cart-wrapper a")

    def get_count_product_in_cart(self):
        self.wait.until(EC.presence_of_element_located((By.ID, "checkout-summary-wrapper")))
        # определяем количество товаров для удаления из корзины (кол-во строк в таблице)
        return self.driver.find_elements_by_css_selector("div#checkout-summary-wrapper td.item")


    def delete_all_prod_from_cart(self, prod_count):
        for i in range(prod_count):
            # определяем элемент исчезновение которого будем ожидать после очередного удаления товара из корзины
            if i != prod_count-1:
                shortcuts = self.smal_prod_icons
                shortcuts[0].click()
            else:
                shortcuts = self.product_image

            products_del = self.del_from_cart_button()
            products_del[0].click()

            # ожидаем исчезновение нужного элемента для продолжения действий
            self.wait.until(EC.staleness_of(shortcuts[0]))

    def wait_for_empty_cart(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#checkout-cart-wrapper a")))
