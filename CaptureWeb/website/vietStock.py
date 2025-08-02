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

class vietStock:
    def __init__(self) -> None:
        self.currRetry = 0
        self.cookieTry = False
    def loginVietStock(self, driver: webdriver.Chrome):
        global RETRY
        try:

            if not self.cookieTry:
                if self.loginVietStockViaCookie(driver):
                    logging.info("Login VietStock successfully via cookies")
                    return True
                driver.delete_all_cookies()
                logging.warning("Failed to login VietStock via cookies")

            logging.info("Trying to login VietStock via credentials")

            if int(config('IS_VIETSTOCK_CHART')) > 0:
                path = "{}/{}/tai-chinh.htm?tab=CHART".format(config('VIETSTOCK'), 'DPM')
                driver.get(path)
                time.sleep(int(config('TIME_WAIT_PAGE')))
                logging.debug("URL: {}".format(path))

                try:
                    
                    # wait for element to loaded 
                    WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "btn-request-call-login"))
                    )
                    # close the popup
                    driver.execute_script("$('#request-login-popup').modal('hide')")
                except:
                    logging.info("popup not found")

                try:
                    elm = driver.find_element(By.XPATH, "//div[contains(@class, 'navbar-login')]//a[contains(@class,'btnlogin')]")
                    elm.click()
                    logging.info(f"Clicked {elm.text}")
                    time.sleep(2)
                    WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "txtEmailLogin"))
                    )
                except:
                    logging.error("Can't find Login button")
                    exit()

                driver.find_element("id", "txtEmailLogin").send_keys(config('LOGIN_VIETSTOCK_USERNAME'))
                driver.find_element("id", "txtPassword").send_keys(config('LOGIN_VIETSTOCK_PASSWORD'))
                driver.find_element("id", "btnLoginAccount").click()

                time.sleep(int(config('TIME_WAIT_PAGE')))

                Cookie().save_cookies(driver, 'cookies_VietStock')
                self.currRetry = 0

        except:
            if self.currRetry < RETRY:
                self.currRetry += 1
                return self.loginVietStock(driver)
            logging.error("[loginVietStock] Login failed. Exceed retry. Exiting...")
            raise LoginFailedException("[loginRobo] Login failed. Exceed retry. Exiting...")

    def loginVietStockViaCookie(self, driver: webdriver.Chrome):
        global RETRY
        try:
            self.cookieTry = True
            # path = "{}".format(config('VIETSTOCK'))
            path = "{}/{}/tai-chinh.htm?tab=CHART".format(config('VIETSTOCK'), 'DPM')
            driver.get(path)
            time.sleep(int(config('TIME_WAIT_PAGE')))
            Cookie().load_cookies(driver, 'cookies_VietStock', False)
            driver.refresh()

            time.sleep(3)

            soup = bs(driver.page_source, 'html.parser')
            accountInfo = soup.find("div", {"class": "divAccountInfo"})
            if accountInfo:
                self.currRetry = 0
                return True
        
            return False

        except Exception as e:
            
            if self.currRetry < RETRY:
                self.currRetry += 1
                return self.loginVietStockViaCookie(driver)

            if not isinstance(e, TimeoutException):
                logging.error("[loginVietStockViaCookie] {}".format(e))
            
            self.currRetry = 0
            return False

    def vietStockChart(self, driver: webdriver.Chrome, line: str):
        if int(config('IS_VIETSTOCK_CHART')) > 0:
            try:
                path = "{}/{}/tai-chinh.htm?tab=CHART".format(config('VIETSTOCK'), line.strip())
                driver.get(path)
                time.sleep(int(config('TIME_WAIT_PAGE')))
                logging.debug("URL: {}".format(path))
                viet_stock_chart_frames = utils.save_viet_stock_chart_frames(driver, line.strip())
                return viet_stock_chart_frames
            except Exception as e:
                logging.error(f"[ERROR] IS_VIETSTOCK_CHART {e}")
                return False
            
        return False
