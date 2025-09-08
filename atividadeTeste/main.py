import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException


class Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def openWebsite(self, url, timeout=15):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return True
        except (WebDriverException, TimeoutException):
            print(f"Falha ao carregar o site: {url}")
            return False

    def testLogin(self):
        driver = self.driver

        # Saucedemo
        if self.openWebsite("https://www.saucedemo.com/"):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
            driver.find_element(By.ID, "user-name").send_keys("standard_user")
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()
            WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
            self.assertIn("inventory.html", driver.current_url)
            print("Login válido com sucesso!")
            driver.delete_all_cookies()

            self.openWebsite("https://www.saucedemo.com/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
            driver.find_element(By.ID, "user-name").send_keys("usuario_invalido")
            driver.find_element(By.ID, "password").send_keys("senha_invalida")
            driver.find_element(By.ID, "login-button").click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h3[@data-test='error']"))
            )
            error_message = driver.find_element(By.XPATH, "//h3[@data-test='error']").text
            self.assertIn("Username and password do not match", error_message)
            print("Saucedemo: login inválido com mensagem de erro correta.")
            driver.delete_all_cookies()

        # The Internet
        if self.openWebsite("https://the-internet.herokuapp.com/login"):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            driver.find_element(By.ID, "username").send_keys("tomsmith")
            driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            WebDriverWait(driver, 10).until(EC.url_contains("/secure"))
            self.assertIn("/secure", driver.current_url)
            print("The Internet: login válido com sucesso!")
            driver.delete_all_cookies()

            self.openWebsite("https://the-internet.herokuapp.com/login")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            driver.find_element(By.ID, "username").send_keys("usuario_invalido")
            driver.find_element(By.ID, "password").send_keys("senha_invalida")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='flash']"))
            )
            error_message = driver.find_element(By.XPATH, "//div[@id='flash']").text
            self.assertIn("Your username is invalid!", error_message)
            print("The Internet: login inválido com mensagem de erro correta.")
            driver.delete_all_cookies()

        # Practice Test Automation
        if self.openWebsite("https://practicetestautomation.com/practice-test-login/"):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            driver.find_element(By.ID, "username").send_keys("student")
            driver.find_element(By.ID, "password").send_keys("Password123")
            driver.find_element(By.ID, "submit").click()
            WebDriverWait(driver, 10).until(EC.url_contains("logged-in-successfully"))
            self.assertIn("logged-in-successfully", driver.current_url)
            print("Practice Test Automation: login válido com sucesso!")
            driver.delete_all_cookies()

            self.openWebsite("https://practicetestautomation.com/practice-test-login/")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            driver.find_element(By.ID, "username").send_keys("usuario_invalido")
            driver.find_element(By.ID, "password").send_keys("senha_invalida")
            driver.find_element(By.ID, "submit").click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='error']"))
            )
            error_message = driver.find_element(By.XPATH, "//div[@id='error']").text
            self.assertIn("Your username is invalid!", error_message)
            print("Practice Test Automation: login inválido com mensagem de erro correta.")
            driver.delete_all_cookies()

        # OrangeHRM
        if self.openWebsite("https://opensource-demo.orangehrmlive.com/"):
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
            driver.find_element(By.NAME, "username").send_keys("Admin")
            driver.find_element(By.NAME, "password").send_keys("admin123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            WebDriverWait(driver, 15).until(EC.url_contains("/dashboard"))
            self.assertIn("/dashboard", driver.current_url)
            print("OrangeHRM: login válido com sucesso!")
            driver.delete_all_cookies()

            self.openWebsite("https://opensource-demo.orangehrmlive.com/")
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
            driver.find_element(By.NAME, "username").send_keys("usuario_invalido")
            driver.find_element(By.NAME, "password").send_keys("senha_invalida")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//p[contains(@class,'oxd-alert-content-text')]"
                ))
            )
            error_message = driver.find_element(By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]").text
            self.assertIn("Invalid credentials", error_message)
            print("OrangeHRM: login inválido com mensagem de erro correta.")
            driver.delete_all_cookies()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
