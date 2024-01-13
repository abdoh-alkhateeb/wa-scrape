import json
import gzip
import pickle
import traceback
from time import sleep
from seleniumwire import webdriver


with open("config.json", "r") as f:
    config = json.load(f)


options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--disable-plugins-discovery")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--profile-directory=Default")
options.add_argument(config["USER_PROFILE_DIRECTORY"])


def main():
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com")
    sleep(5)

    try:
        with open("session.gz", "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
    except FileNotFoundError:
        sleep(60)
        print(driver.get_cookies())
        if not driver.get_cookies():
            raise Exception("User didn't scan QR code")
        with gzip.open("session.gz", "wb") as f:
            pickle.dump(driver.get_cookies(), f)
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()
