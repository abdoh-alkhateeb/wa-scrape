import os
import tarfile
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class WhatsAppScraper:
    def __init__(self):
        os.environ["TMPDIR"] = "temp"

        options = webdriver.FirefoxOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins-discovery")

        WhatsAppScraper.inflate_session_file()
        options.add_argument("--user-data-dir=temp/user_data")

        self.driver = webdriver.Firefox(options=options)
        self.authenticate()

        self.driver.get("https://web.whatsapp.com")

        sleep(30)

    @staticmethod
    def inflate_session_file():
        try:
            if not os.path.exists("temp/user_data"):
                with tarfile.open("session.tar.gz", "r:gz") as tar:
                    tar.extractall(path=".")
        except FileNotFoundError:
            pass

    def authenticate(self):
        try:
            self.driver.get("https://web.whatsapp.com")

            wait = WebDriverWait(self.driver, 60)

            _ = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span")))
        except TimeoutException:
            raise Exception("User couldn't be authenticated")

    @staticmethod
    def deflate_session_file():
        with tarfile.open("session.tar.gz", "w:gz") as tar:
            tar.add("temp/user_data")

    def cleanup(self):
        self.driver.quit()
        WhatsAppScraper.deflate_session_file()
