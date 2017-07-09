import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def test_example():
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
#    driver = webdriver.Remote("http://denkukushkin1:2sJgx7wjfVhe9pAtuo1Q@hub.browserstack.com:80/wd/hub", \
#                              desired_capabilities={'browser': 'chrome', 'version': "55", 'platform': "WIN8"})

    driver.get('http://www.google.com/')

    if not "Google" in driver.title:
        raise Exception("Unable to load google page!")
    elem = driver.find_element_by_name("q")
    elem.send_keys("BrowserStack")
    elem.submit()
    print(driver.title)
    driver.quit()


def test_example2():
    # ------------------------------
    # The actual test scenario: Test the codepad.org code execution service.

    driver = webdriver.Remote("http://denkukushkin1:2sJgx7wjfVhe9pAtuo1Q@hub.browserstack.com:80/wd/hub", \
                              desired_capabilities={'browser': 'chrome', 'version': "55", 'platform': "WIN8"})
    # Go to codepad.org
    driver.get('http://codepad.org')

    # Select the Python language option
    python_link = driver.find_elements_by_xpath("//input[@name='lang' and @value='Python']")[0]
    python_link.click()

    # Enter some text!
    text_area = driver.find_element_by_id('textarea')
    text_area.send_keys("print 'Hello,' + ' World!'")

    # Submit the form!
    submit_button = driver.find_element_by_name('submit')
    submit_button.click()

    # Close the browser!
    driver.quit()

test_example2()
