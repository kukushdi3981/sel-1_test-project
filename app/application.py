from selenium import webdriver

from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.block_cart_page import BlockCartPage
from pages.cart_page import CartPage

class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()
#        self.driver = webdriver.Ie()
        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.block_cart_page = BlockCartPage(self.driver)
        self.cart_page = CartPage(self.driver)

    def quit(self):
        self.driver.quit()

    def back(self):
        self.driver.back()

    def open_cart(self):
        self.block_cart_page.cart_link_button.click()

    def add_product_to_cart(self, text):
        self.main_page.open()

        # ищем продукты и берем произвольный продукт для добавления в корзину
        self.main_page.select_product()

        self.product_page.select_product_size()
        self.product_page.quantity_input.clear()
        self.product_page.quantity_input.send_keys("1")
        self.product_page.add_to_cart_button.click()

        # ожидаем помещения текста в корзину (увеличения количества товаров в корзине на 1)
        self.block_cart_page.wait_adding_prod_to_cart(text)

    def delete_products_from_cart(self):
    #   определяем количество товаров для удаления из корзины (кол-во строк в таблице)
        rows = self.cart_page.get_count_product_in_cart()
        self.cart_page.delete_all_prod_from_cart(len(rows))

    #   ожидаем очистки корзины и переходим на главную страницу магазина
        self.cart_page.wait_for_empty_cart()
        self.cart_page.back_main_page_link.click()
