import os
import shutil
import tarfile
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


USER_PROFILE_PATH = "temp/user-data"


class WhatsAppScraper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins-discovery")

        WhatsAppScraper.inflate_session_file()
        options.add_argument(f"--user-data-dir={USER_PROFILE_PATH}")

        self.driver = webdriver.Chrome(options=options)
        self.authenticate()

        self.driver.get("https://web.whatsapp.com")

        sleep(30)

    @staticmethod
    def inflate_session_file():
        try:
            if os.path.exists(USER_PROFILE_PATH):
                shutil.rmtree(USER_PROFILE_PATH)

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
        try:
            with tarfile.open("session.tar.gz", "w:gz") as tar:
                tar.add(USER_PROFILE_PATH)
        except FileNotFoundError:
            os.remove("session.tar.gz")

    def cleanup(self):
        self.driver.quit()
        WhatsAppScraper.deflate_session_file()
