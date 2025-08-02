import time
import logging
from service.exceptions import LoginFailedException
import utils
import coloredlogs


from bs4 import BeautifulSoup as bs
from selenium import webdriver
from decouple import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from service import Cookie

coloredlogs.install()

RETRY = 1
currRetry = 0
cookieTry = False

class roboCK:
    def __init__(self) -> None:
        self.currRetry = 0
        self.cookieTry = False
    def loginRobo(self, driver: webdriver.Chrome):
        try:

            if not self.cookieTry:
                if self.loginRoboViaCookie(driver):
                    print("Login Robo successfully via cookies")
                    return True
                
            logging.error("Failed to login Robo via cookies")
            logging.info("Login Robo via credentials")

            driver.get("{}/#/auth/login".format(config('BASE_URL')))
            driver.find_element("id", "inputEmailAddress").send_keys(config('LOGIN_USERNAME'))
            driver.find_element("id", "inputPassword").send_keys(config('LOGIN_PASSWORD'))
            driver.find_element(By.XPATH, "//button").click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@class="card mb-3 card-box-shadow"]')))
            except TimeoutException:
                logging.error("TimeoutException")
                driver.refresh()
                try:
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@class="card mb-3 card-box-shadow"]')))
                except Exception: 
                    raise("Cannot find element")

        except:
            if self.currRetry < RETRY:
                self.currRetry += 1
                return self.loginRobo(driver)
            logging.error("[loginRobo] Login failed. Exceed retry. Exiting...")
            raise LoginFailedException("[loginRobo] Login failed. Exceed retry. Exiting...")

        time.sleep(3)

        Cookie().save_cookies(driver, 'cookies_Robo', True)
        self.currRetry = 0

    def loginRoboViaCookie(self, driver: webdriver.Chrome):
        global RETRY
        try:
            self.cookieTry = True
            driver.get("{}".format(config('BASE_URL')))

            time.sleep(3)

            if not Cookie().load_cookies(driver, 'cookies_Robo', True): return False

            driver.refresh()

            time.sleep(3)
            
            if driver.current_url == "https://robotchungkhoan.nududo.com/#/auth/login":
                return False

            soup = bs(driver.page_source, 'html.parser')
            if not soup.find("input", {"id": "inputEmailAddress"}):
                return True

            return False
        except Exception as e: 

            if not isinstance(e, TimeoutException):
                logging.error("[loginRoboViaCookie] {}".format(e))

            if self.currRetry < RETRY:
                self.currRetry += 1
                logging.error("[loginRoboViaCookie] Login failed. Retrying...")
                return self.loginRoboViaCookie(driver)

            self.currRetry = 0
            return False

    def robotChart(self, driver: webdriver.Chrome, line: str):
        try:
            imagePaths = []
            path = "{}/#/phantichcophieu?stockcode={}".format(config('BASE_URL'), line.strip())
            driver.get(path)
            time.sleep(int(config('TIME_WAIT_PAGE')))
            logging.debug("URL: {}".format(path))
            utils.removeSocialContacts(driver)
            stock_nanlysis_frames = utils.save_stock_analysis_frames(driver, line.strip())
            imagePaths.extend(stock_nanlysis_frames)

            if int(config('IS_CANSLIM')) > 0:
                try:
                    path = "{}/#/canslimsepa".format(config('BASE_URL'))
                    driver.get(path)
                    utils.removeSocialContacts(driver)
                    time.sleep(int(config('TIME_WAIT_PAGE')))
                    logging.debug("URL: {}".format(path))
                    driver.find_element(By.NAME, "search").send_keys(line.strip())
                    canslim_frames = utils.save_canslim_frames(driver, line.strip())
                    imagePaths.extend(canslim_frames)

                except Exception as e:
                    logging.error(f"[ERROR] IS_CANSLIM {e}")

            if int(config('IS_STOCK_RATING')) > 0:
                try:
                    path = "{}/#/xephangcophieu".format(config('BASE_URL'))
                    driver.get(path)
                    utils.removeSocialContacts(driver)
                    time.sleep(int(config('TIME_WAIT_PAGE')))
                    logging.debug("URL: {}".format(path))
                    driver.find_element(By.NAME, "search").send_keys(line.strip())
                    stock_rating_frames = utils.save_stock_rating_frames(driver, line.strip())
                    imagePaths.extend(stock_rating_frames)

                except Exception as e:
                    logging.error(f"[ERROR] IS_STOCK_RATING {e}")

            return imagePaths
        except Exception as e:
            logging.error("[robotChart] {}".format(e))
