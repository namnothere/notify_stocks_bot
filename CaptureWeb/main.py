import os
import threading
import time
import logging
import utils
import requests
import coloredlogs

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from decouple import config
from datetime import datetime
from website import *

coloredlogs.install()
# logging.basicConfig(filename='C:/Stock_Python/CaptureWeb_BOT/logs/std.log',
logging.basicConfig(filename=os.getcwd() + '/logs/std.log',
                    filemode='w',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def initBrowser():
    logging.debug('Install chrome driver')
    # chrome_driver_path = ChromeDriverManager(driver_version='114.0.5735.90').install()
    chrome_driver_path = ChromeDriverManager(driver_version='121.0.6167.184').install()
    # chrome_driver_path = 'C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'
    # chrome_driver_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    service = Service(chrome_driver_path)

    # Setup chrome options
    logging.debug('Setup chrome options')
    # ua = UserAgent()
    # user_agent = ua.random
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    # options.add_argument('--incognito')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    mainprofile = config('MAIN_PROFILE')
    options.add_argument(f"--user-data-dir={mainprofile}")

    #options.add_argument('--disable-gpu')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument("log-level=3") 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(30)
    driver.maximize_window()
    return driver

def close_all_tabs(driver: webdriver.Chrome):
    try:
        tab_handles = driver.window_handles
        # Loop through the handles and close each tab
        for handle in tab_handles:
            driver.switch_to.window(handle)
            driver.close()
        driver.quit()
    except:
        pass

def quit(driver: webdriver.Chrome):
    try:
        close_all_tabs(driver)
    except:
        pass
    finally:
        exit()

def take_full_page_screenshot(returnImage: bool = False, ticker: str = None):
    try:
        # Install chrome driver
        driver = initBrowser()

        roboFailed = True
        vietstockFailed = True
        wichartFailed = True

        vt = vietStock()
        rb = roboCK()
        wc = wiChart()

        if int(config('LOGIN_VIETSTOCK')) <= 0 and int(config('LOGIN_ROBO')) <= 0 and int(config('LOGIN_WICHART')) <= 0:
            logging.info("Skipping all login. Exiting...")
            quit(driver)

        # LOGIN VIETSTOCK NEW PAGE
        try:
            if int(config('LOGIN_VIETSTOCK')) > 0:
                logging.info("LOGIN VIETSTOCK NEW PAGE")
                vt.loginVietStock(driver)
                vietstockFailed = False
            else:
                logging.info("Skipping loginVietStock")
        except LoginFailedException:
            pass
            #quit(driver)
        except Exception as e:
            logging.error("[loginVietStock] {}".format(e))
        # END LOGIN VIETSTOCK NEW PAGE

        # LOGIN ROBOT PAGE
        try:
            if int(config('LOGIN_ROBO')) > 0:
                logging.info("LOGIN ROBOT PAGE")
                rb.loginRobo(driver)
                roboFailed = False
            else: logging.info("Skipping loginRobo")
        except LoginFailedException:
            # quit(driver)
            roboFailed = True
        except Exception as e:
            logging.error("[loginRobo] {}".format(e))
        # END LOGIN ROBOT PAGE

        # LOGIN WICHART
        try:
            if int(config('LOGIN_WICHART')) > 0:
                logging.info("LOGIN WICHART")
                wc.loginWichart(driver)
                wichartFailed = False
            else: logging.info("Skipping loginWichart")
        except LoginFailedException:
            logging.error("[loginWichart] LoginFailedException")
            roboFailed = True
            #quit(driver)
        except Exception as e:
            logging.error("[loginWichart] {}".format(e))
        # END LOGIN WICHART

        # Using readlines()
        logging.debug("Starting read filter stock file")
        filterStockFile = open(config('FILTER_STOCK_FILE_PATH'), 'r')
        if not ticker:
            Lines = filterStockFile.readlines()
        else: Lines = [ticker]

        isScheduleLoop = 1
        while isScheduleLoop > 0:

            imagePaths = []

            FROM_TIME = config('FROM_TIME')
            TO_TIME = config('TO_TIME')
            now = datetime.now()
            NOW_TIME = now.strftime("%H:%M:%S")

            logging.debug(
                "FROM_TIME: {}. TO_TIME: {}. NOW_TIME: {}. FROM_TIME < NOW_TIME < TO_TIME: {}".format(FROM_TIME, TO_TIME,
                                                                                                    NOW_TIME,
                                                                                                    FROM_TIME < NOW_TIME < TO_TIME))
            if FROM_TIME < NOW_TIME < TO_TIME:
                utils.remove_files(config('TMP_SAVE_IMAGES_PATH'))

                for line in Lines:
                    try:
                        # ROBO CHART
                        try:
                            if int(config('IS_ROBO_CHART')) > 0 and int(config('LOGIN_ROBO')) > 0 and roboFailed == False:
                                rb.robotChart(driver, line.strip())
                        except Exception as e:
                            logging.error("[take_full_page_screenshot-robotChart] {}".format(e))
                        # END ROBO CHART

                        # VIETSTOCK CHART
                        try:
                            if int(config('IS_VIETSTOCK_CHART')) > 0 and int(config('LOGIN_VIETSTOCK')) > 0 and vietstockFailed == False:
                                vt.vietStockChart(driver, line.strip())
                        except Exception as e:
                            logging.error("[take_full_page_screenshot-vietStockChart] {}".format(e))
                        # END VIETSTOCK CHART

                        # WINCHART
                        try:
                            if int(config('LOGIN_WICHART')) > 0 and wichartFailed == False:
                                
                                if int(config('IS_WICHART_12CHARTS')) > 0:
                                    wc.wichartChart(driver, line.strip())

                                if int(config('IS_WICHART_ANALYSIS')) > 0:
                                    wc.analysis_Reports(driver, line.strip())

                        except Exception as e:
                            logging.error("[take_full_page_screenshot-wichartChart] {}".format(e))
                        # END WINCHART

                        try:
                            thisSessionImages = utils.merge_files(line.strip(), returnImage)
                            imagePaths.extend(thisSessionImages) if thisSessionImages else None
                        except Exception as e:
                            logging.error("[take_full_page_screenshot-merge_files] {}".format(e))
                        
                    except Exception as e:
                        logging.error("[take_full_page_screenshot-Lines] {}".format(e))

            isScheduleLoop = int(config('IS_SCHEDULE'))
            if isScheduleLoop > 0:
                logging.debug("TIME SLEEP: {} (s)".format(int(config('TIME_SCAN'))))
                time.sleep(int(config('TIME_SCAN')))

        close_all_tabs(driver)
        
        if returnImage:
            return imagePaths
    except Exception as e:
        logging.error("[take_full_page_screenshot] {}".format(e))
        # quit(driver)
        try:
            driver.quit()
        except: pass
        raise Exception(e)
    # finally:

def postImage(imagePath: str):
    try:
        with open(os.path.join(target_dir, imagePath), 'rb') as image:
            payload = {'chatId': chat_id,
                        'caption': ticker}
            files=[
                ('image',(f"{ticker}.png", image,'image/jpeg'))
            ]
            response = requests.request("POST", url, data=payload, files=files)
            logging.info("Sent image to chat_id: {}".format(chat_id))
            print(response.content)
        os.remove(os.path.join(target_dir, imagePath))
        logging.info(f"Removed: {os.path.join(target_dir, imagePath)}")
    except Exception as e:
        logging.error(f"[postImage-{imagePath}] {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("--chat_id", action="store", dest="chat_id")
    parser.add_argument("--ticker", action="store", dest="ticker")

    args = parser.parse_args()
    try:
        chat_id = args.chat_id
    except: chat_id = None
    try:
        ticker = args.ticker
    except: ticker = None

    if not chat_id and not ticker:
        try:
            take_full_page_screenshot()
        except Exception as e:
            logging.error("[MAIN-1] {}".format(e))
    elif not chat_id or not ticker:
        logging.error("[MAIN] Please provide chat_id and ticker")
        exit()

    elif chat_id and ticker:
        url = "http://localhost:3000/executer/"
        logging.info(f"args {args}")
        try:
            imagePaths = take_full_page_screenshot(returnImage=True, ticker=ticker)
            target_dir = config('SAVE_IMAGES_PATH')

            threads: list[threading.Thread] = []

            for imagePath in imagePaths:
                t = threading.Thread(target=postImage, args=(imagePath,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            del threads

        except Exception as e:
            payload = {'chatId': chat_id,
                        'error': f"Capture failed {imagePaths}"}
            logging.error("[MAIN-2] {}".format(e))
            response = requests.request("POST", url, data=payload)
