import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
BASE_URL = "https://www.saucedemo.com"


class TestSwagLabsFunctional(unittest.TestCase):

    def setUp(self):
        service = Service(CHROME_DRIVER_PATH)

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

        self.driver.get(BASE_URL)
        time.sleep(3) 
    def tearDown(self):
        time.sleep(3)  
        self.driver.quit()

    def test_01_login_with_valid_credentials(self):
        """Verify user can login with valid credentials"""

        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(3)

        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(3)

        self.driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        title = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title"))
        )

        self.assertEqual(title.text, "Products")
        self.assertIn("inventory.html", self.driver.current_url)
        time.sleep(3)

    def test_02_login_with_locked_user(self):
        """Verify error message for locked out user"""

        self.driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        time.sleep(3)

        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(3)

        self.driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        error_message = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )

        self.assertEqual(
            error_message.text,
            "Epic sadface: Sorry, this user has been locked out."
        )
        time.sleep(3)

    def test_03_add_product_to_cart(self):
        """Verify product can be added to cart"""

        self.driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(3)

        self.driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(3)

        self.driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        add_to_cart_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        )
        add_to_cart_btn.click()
        time.sleep(3)

        cart_badge = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
        )
        self.assertEqual(cart_badge.text, "1")
        time.sleep(3)

        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(3)

        product_name = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        )
        self.assertEqual(product_name.text, "Sauce Labs Backpack")
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
