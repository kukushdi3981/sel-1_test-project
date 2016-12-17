import pytest
from app.application import Application

def test_work_with_cart(app = Application()):
    for iter in range(3):
        app.add_product_to_cart(str(iter+1))
        app.back()
    app.open_cart()
    app.delete_products_from_cart()
    app.quit()
