import os
import pickle
import logging
import coloredlogs

from selenium import webdriver

coloredlogs.install()

class Cookie:
    def __init__(self) -> None:
        self.module_path = os.path.dirname(os.path.abspath(__file__))
        self.dir_path = os.path.dirname(self.module_path)
        self.path = os.path.join(self.dir_path, "cookies")
        self.init_cookies()

    def init_cookies(self):
        os.makedirs(self.path, exist_ok=True)

    def save_cookies(self, driver: webdriver.Chrome, service: str = None, execute_script: bool = False):
        """Save cookies from a Selenium WebDriver to a file."""
        try:
            filename = f'{service}.pkl'
            with open(os.path.join(self.path, filename), 'wb') as file:
                if not execute_script:
                    pickle.dump(driver.get_cookies(), file)
                    logging.info(f'Save cookies from Selenium to {filename}.')
                    return True

                cookies = driver.execute_script(f"return window.localStorage.getItem('users');")
                pickle.dump(cookies, file)

                logging.info(f'Save cookies from Selenium to {filename}.')

                return True
        except Exception as e:
            logging.error("[save_cookies] {}".format(e)) 
            return False

    def saveReqCookies(self, data: dict, service: str = None):
        filename = f'{service}.pkl'
        with open(os.path.join(self.path, filename), 'wb') as file:
            pickle.dump(data, file)

    def savePartialCookies(self, driver: webdriver.Chrome, service: str = None, cookie_name: str = None):
        filename = f'{service}.pkl'
        cookies = driver.get_cookies()
        logging.info(cookies)
        for c in cookies:
            if c.get('name') != cookie_name:
                cookies.remove(c)
        with open(os.path.join(self.path, filename), 'wb') as file:
            pickle.dump(c, file)
        
    def load_cookies(self, driver: webdriver.Chrome, service: str = None, execute_script: bool = False):
        try:
            filename = f'{service}.pkl'
            """Load cookies from a file and set them in a Selenium WebDriver."""
            logging.info(os.path.join(self.path, filename))
            with open(os.path.join(self.path, filename), 'rb') as file:
                cookies = pickle.load(file)

            if not execute_script:
                for cookie in cookies:
                    driver.add_cookie(cookie)

                logging.info(f"Cookies loaded. {filename}")
                return True
            
            driver.execute_script(f"localStorage.setItem('users', '{cookies}');")
            logging.info(f"Cookies loaded. {filename}")
            return True
        except Exception as e:
            logging.error("[load_cookies] {}".format(e)) 
            return False
