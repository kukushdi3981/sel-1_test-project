import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()  # Optional argument, if not specified will search path.
#    wd = webdriver.Ie()

    print(wd.capabilities)
#    wd.implicitly_wait(10)
    request.addfinalizer(wd.quit)
    return wd

def Open_registration_page(driver):
    driver.find_element_by_css_selector("form[name='login_form'] a").click()

def User_registration(driver, dictionary):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "create-account")))


#   fill registrtion form fields
    driver.find_element_by_css_selector("div#create-account input[name='firstname']").send_keys(dictionary['FirstName'])
    driver.find_element_by_css_selector("div#create-account input[name='lastname']").send_keys(dictionary['LastName'])
    driver.find_element_by_css_selector("div#create-account input[name='address1']").send_keys(dictionary['Adress'])
    driver.find_element_by_css_selector("div#create-account input[name='postcode']").send_keys(dictionary['Postcode'])
    driver.find_element_by_css_selector("div#create-account input[name='city']").send_keys(dictionary['City'])
    driver.find_element_by_css_selector("div#create-account input[name='email']").send_keys(dictionary['Email'])
    driver.find_element_by_css_selector("div#create-account input[name='phone']").send_keys(dictionary['Phone'])
    driver.find_element_by_css_selector("div#create-account input[name='password']").send_keys(dictionary['Password'])
    driver.find_element_by_css_selector("div#create-account input[name='confirmed_password']").send_keys(dictionary['Password'])
    driver.find_element_by_css_selector("div#create-account input[type='checkbox']").click()

#   submit registrtion
    driver.find_element_by_css_selector("div#create-account button[type='submit']").click()


def Logout(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-account")))

    driver.find_element_by_css_selector("div.content a[href$=logout]").click()

def Login(driver, dictionary):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "box-account-login")))

#   fill login fields
    driver.find_element_by_css_selector("form[name='login_form'] input[name='email']").send_keys(dictionary['Email'])
    driver.find_element_by_css_selector("form[name='login_form'] input[name='password']").send_keys(dictionary['Password'])

    driver.find_element_by_css_selector("form[name='login_form'] button[name='login']").click()



def test_User_registration(driver):
    user_info = {
        "FirstName": "Jack",
        "LastName": "Hunter",
        "Postcode": "146263",
        "City": "Moscow",
        "Adress": "Street Lee",
        "Email": "",
        "Phone": "4951112233",
        "Password": "Qwerty",
    }

    user_info['Email'] = user_info['FirstName'] + str(random.randint(1,9)) + user_info['LastName'] +\
                         str(random.randint(1,9)) + "@gmail.com"

    user_info['Password'] = user_info['Password'] + str(random.randint(1,99))

    driver.get('http://localhost/litecart/')
    Open_registration_page(driver)
    User_registration(driver, user_info)
    Logout(driver)
    Login(driver, user_info)
    Logout(driver)

