import time
import logging
from service.exceptions import LoginFailedException
import utils
import coloredlogs
import requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from decouple import config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from service import *
from selenium import webdriver

coloredlogs.install()

RETRY = 1

class wiChart:

    def __init__(self) -> None:
        self.currRetry = 0
        self.cookieTry = False

    def getTokenViaRequest(self):
        json_data = {
            'email': 'ngviendong@gmail.com',
            'password': 'Dora#789',
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'v': 'v1',
        }

        response = requests.post(
            'https://wichart.vn/wichartapi/wichart/taikhoan/dangnhap',
            headers=headers,
            json=json_data,
        )

        res = response.json()
        if 'token' in res:
            Cookie().saveReqCookies(res, 'cookies_Wichart')

    def manipulateDeviceToken(self, driver: webdriver.Chrome):
        if not config('WICHART_DEVICE_TOKEN') or config('WICHART_DEVICE_TOKEN') == '':
            logging.warn("DeviceToken not found")
            return False

        for c in driver.get_cookies():
            if c['name'] == 'deviceToken':
                c['value'] = config('WICHART_DEVICE_TOKEN')


    def loginWichart(self, driver: webdriver.Chrome):
        global RETRY
        try:
            if not self.cookieTry and int(config('IS_WICHART_COOKIE')) > 0:
                if self.loginWichartViaCookie(driver):
                    logging.info("Login WiChart successfully via cookies")
                    return True
                logging.error("Failed to login WiChart via cookies")
            
            driver.delete_all_cookies()
                
            logging.info("Login WiChart via credentials")
            #self.manipulateDeviceToken(driver)

            driver.get("{}/login".format(config('WINCHART_BASE_URL')))
            driver.find_element(By.XPATH, "//input[@name='email']").send_keys(config('LOGIN_WICHART_USERNAME'))
            driver.find_element(By.XPATH, "//input[@name='password']").send_keys(config('LOGIN_WICHART_PASSWORD'))
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "MuiAvatar-root")]')))
            except TimeoutException:
                logging.error("TimeoutException")
                driver.refresh()
                try:
                    WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "MuiAvatar-root")]')))
                except Exception: 
                    raise Exception("Cannot find element")

        except:
            if self.currRetry < RETRY:
                self.currRetry += 1
                return self.loginWichart(driver)
            logging.error("[loginWichart] Login failed. Exceed retry. Exiting...")
            raise LoginFailedException("[loginWichart] Login failed. Exceed retry. Exiting...")

        time.sleep(3)

        Cookie().save_cookies(driver, 'cookies_Wichart', False)
        self.currRetry = 0

    def loginWichartViaCookie(self, driver: webdriver.Chrome):
        try:
            # return False
            self.cookieTry = True
            driver.get("{}".format(config('WINCHART_BASE_URL')))

            time.sleep(1)

            if not Cookie().load_cookies(driver, 'cookies_Wichart', False): return False

            driver.refresh()

            time.sleep(2)

            token = driver.execute_script('function getCookie(){let i=i=>i.split("="),o=i=>"wtoken"===i[0];return(null===(e=document.cookie.split("; ").map(i).find(o))||void 0===e?void 0:e.slice(1).join(""))||""} return getCookie();')

            if not token or str(token).strip() == "":
                self.currTry = 0
                return False
            
            if driver.current_url == "https://wichart.vn/login":
                return False

            soup = bs(driver.page_source, 'html.parser')
            if not soup.find("input", {"id": ":r1:"}):
                return True

            return False
        except Exception as e: 

            if not isinstance(e, TimeoutException):
                logging.error("[loginWichartViaCookie] {}".format(e))

            if self.currRetry < RETRY:
                self.currRetry += 1
                logging.error("[loginWichartViaCookie] Login failed. Retrying...")
                return self.loginWichartViaCookie(driver)

            self.currRetry = 0
            return False

    def wichartChart(self, driver: webdriver.Chrome, line: str):
        try:
            if int(config('IS_WICHART_12CHARTS')) <= 0: return True

            path = "https://wichart.vn/{}?slug={}&tab=financial-charts".format(line.strip(), line.strip())
            driver.get(path)
            time.sleep(int(config('TIME_WAIT_PAGE')) * 2)
            logging.debug("URL: {}".format(path))

            imagePaths = utils.wi_chart_chart_frames(driver, line.strip())
            return imagePaths

        except Exception as e:
            logging.error("[WichartChart] {}".format(e))

    def analysis_Reports(self, driver: webdriver.Chrome, line: str):
        try:
            if int(config('IS_WICHART_ANALYSIS')) <= 0: return True
            path = "https://wichart.vn/{}?tab=analysis-reports".format(line.strip())
            driver.get(path)
            time.sleep(int(config('TIME_WAIT_PAGE')) * 2)

            logging.debug("URL: {}".format(path))
            imagePaths = utils.wi_chart_analysis_report(driver, line.strip())
            return imagePaths

        except Exception as e:
            logging.error("[analysis_Reports] {}".format(e))
        

    def quit(self, driver: webdriver.Chrome):
        try:
            driver.quit()
        except: pass
        finally: exit()
