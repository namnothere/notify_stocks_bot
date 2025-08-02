import io
import time
import os
import shutil
import service.frames as frames
import service.images as images
import logging, coloredlogs

from selenium import webdriver
from decouple import config
from PIL import Image
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

coloredlogs.install()
def save_element_screenshot(driver: webdriver.Chrome, path: str = '/tmp/screenshot.png', element: str = '', webelement: WebElement = None) -> bool:
    try:
        if not webelement:
            driver.set_window_size(int(config('BROWSER_WIDTH')), int(config('BROWSER_HEIGHT')))
            time.sleep(5)
            driver.find_element(By.XPATH, element).screenshot(path)
            logging.info("Screenshot: {}".format(path))
        else:
            try:
                time.sleep(1)
                # webelement.screenshot(path)
                screenshot = webelement.screenshot_as_png
                image = Image.open(io.BytesIO(screenshot))

                element_width = webelement.size['width']
                element_height = webelement.size['height']

                roi = (0, 0, element_width, element_height)

                # Crop the screenshot to the ROI
                cropped_image = image.crop(roi)
                cropped_image.save(path)

                logging.info("Screenshot: {}".format(path))
                return path

            except Exception as e:
                logging.error("[save_element_screenshot webelement] {}".format(e))
                return False
        return True
    except Exception as e:
        driver.save_screenshot(f"[save_element_screenshot] ERROR.png")
        logging.error("[save_element_screenshot] {}".format(e))
        return False

# def zoomOut(driver: webdriver.Chrome):
    
#     original_handle = driver.current_window_handle
#     driver.execute_script("window.open('');")
#     time.sleep(1)
#     driver.switch_to.window(driver.window_handles[-1])
#     driver.get('chrome://settings/')
#     zoom = 0.8 #for example 0.5, or 1.5 or 2.0 and so on
#     try:
#         driver.execute_script(f'chrome.settingsPrivate.setDefaultZoom({zoom});')
#     except Exception as e:
#         input("[zoomOut] {}".format(e))
    
#     driver.close()
#     time.sleep(1)
#     driver.switch_to.window(original_handle)

# def zoomIn(driver: webdriver.Chrome):
#     original_handle = driver.current_window_handle
#     driver.execute_script("window.open('');")
#     driver.switch_to.window(driver.window_handles[-1])
#     time.sleep(1)
#     driver.get('chrome://settings/')
#     zoom = 1
#     driver.execute_script(f'chrome.settingsPrivate.setDefaultZoom({zoom});')
#     driver.close()
#     time.sleep(1)
#     driver.switch_to.window(original_handle)

def save_stock_analysis_frames(driver: webdriver.Chrome, stockCode: str) -> list[str]:
    # zoomOut(driver)
    xpathIds = frames.get_xpath_ids()
    imagePaths = []

    # while input("Do you want to use custom xpath? (y/n) ") != '':
    #     xpath = input("Enter xpath: ")
    #     customScreenshot(driver, xpath)

    for idx, xpathId in enumerate(xpathIds):
        # if idx == 0:
        #     pies_chart_list = []
        #     for i in range(1, 5):
        #         tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_PIE_SUM_FA_2_{xpathId}_{i}.png")
        #         xpathElement = "{}/div[{}]/div[{}]".format(config('XPATH_SECTION'), xpathId, i)
        #         pie = WebDriverWait(driver, 5).until(
        #             EC.visibility_of_element_located((By.XPATH, xpathElement))
        #         )
        #         path = save_element_screenshot(driver, tmpPath, xpathElement, pie)
        #         pies_chart_list.append(path)

        #     tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_SUM_FA_2_{xpathId}.png")
        #     pies_paths = merge_files_horizontal(pies_chart_list, tmpPath)
        #     imagePaths.extend(pies_paths)
        #     continue
        tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_SUM_FA_2_{xpathId}.png")
        xpathElement = "{}/div[{}]".format(config('XPATH_SECTION'), xpathId)

        # scroll to bottom
        ele = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, xpathElement))
        )

        path = save_element_screenshot(driver, tmpPath, xpathElement, ele)
        imagePaths.append(path)
    return imagePaths

def save_canslim_frames(driver: webdriver.Chrome, stockCode: str) -> list[str]:
    # tmpPath = "{}/{}_CAN_SLIM.png".format(config('TMP_SAVE_IMAGES_PATH'), stockCode)
    tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_CAN_SLIM.png")
    ele = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, config('XPATH_CANSLIM')))
        )
    path = save_element_screenshot(driver, tmpPath, config('XPATH_CANSLIM'), ele)
    return [path]

def save_stock_rating_frames(driver: webdriver.Chrome, stockCode: str) -> list[str]:
    # tmpPath = "{}/{}_STOCK_RATING.png".format(config('TMP_SAVE_IMAGES_PATH'), stockCode)
    tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_STOCK_RATING.png")
    ele = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, config('XPATH_STOCK_RATING')))
    )
    path = save_element_screenshot(driver, tmpPath, config('XPATH_STOCK_RATING'), ele)
    return [path]

def save_viet_stock_chart_frames(driver: webdriver.Chrome, stockCode: str) -> list[str]:
    # tmpPath = "{}/{}_VIETSTOCK_CHART.png".format(config('TMP_SAVE_IMAGES_PATH'), stockCode)
    tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_VIETSTOCK_CHART.png")
    try:
        driver.execute_script("var header = document.getElementById('page-menu'); if (header) header.remove();")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, config('XPATH_VIETSTOCK_CHART')))
        )
    except:
        pass
    path = save_element_screenshot(driver, tmpPath, config('XPATH_VIETSTOCK_CHART'))
    return [path]

def removeHeader(driver: webdriver.Chrome):
    try:
        header = driver.find_element(By.XPATH, '//header')
        driver.execute_script("arguments[0].remove();", header)
    except:
        pass
    try:
        companyTab = driver.find_element(By.XPATH, '//div[@id="company-tab"]')
        driver.execute_script("arguments[0].remove();", companyTab)
    except: pass
    try:
        breadcrumb = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]')
        driver.execute_script("arguments[0].remove();", breadcrumb)
    except:
        pass

def wi_chart_chart_frames(driver: webdriver.Chrome, stockCode: str) -> list[str]:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, config('XPATH_WICHART_CHART')))
        )
    except:
        pass

    removeHeader(driver)

    try:
        for _ in range(0, 2000, 500):
            # scroll to bottom
            ActionChains(driver) \
                .scroll_by_amount(0, 500)\
                .perform()
            time.sleep(1)
    except Exception as e:
        logging.error("[wi_chart_chart_frames] {}".format(e))

    # ALL CONTAINERS
    containers: list[WebElement] = driver.find_elements(By.XPATH, config('XPATH_WICHART_CHART'))
    imagePaths = []
    for idx, chart in enumerate(containers):
        tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_FA_8_{idx}.png")
        try:
            chart.location_once_scrolled_into_view
            # logging.info("Loc: {}".format(loc))
            path = save_element_screenshot(driver, tmpPath, webelement=chart)
            imagePaths.append(path)
        except Exception as e:
            logging.error("[wi_chart_chart_frames] {}".format(e))

    return imagePaths

def wi_chart_analysis_report(driver: webdriver.Chrome, stockCode: str) -> list[str]:
    try:
        analysis_table: WebElement = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, config('XPATH_WICHART_ANALYSIS')))
        )

        removeHeader(driver)

        tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_WICHART_ANALYSIS_REPORT.png")

        # remove the big table report
        try:
            table = analysis_table.find_element(By.CSS_SELECTOR, config('CSS_ANALYSIS_TABLE'))
            driver.execute_script("arguments[0].remove();", table)
        except: pass

        time.sleep(int(config('WI_CHART_WAIT')))

        full_page = driver.find_element(By.XPATH, config('XPATH_WICHART_INFO_AND_ANALYSIS'))

        path = save_element_screenshot(driver, tmpPath, webelement=full_page)
        return [path]

    except Exception as e:
        driver.save_screenshot("[wi_chart_analysis_report] ERROR.png")
        logging.error("[wi_chart_analysis_report] {}".format(e))
        return []

def merge_files_horizontal(imagesPathList: list, tmpPath: str):
    if len(imagesPathList) == 0:
        return []
    tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"TEST.png")

    imagesList = [Image.open(imagePath) for imagePath in imagesPathList]

    chartPies = images.concat_images_horizontally(imagesList)
    logging.info(f"chartPies: {chartPies}")
    if chartPies:
        chartPies.save(tmpPath)
        logging.info(f"Saved robochart pies: {tmpPath}")
        return [tmpPath]
    return []

def merge_files(stockCode: str, returnImage: bool = False):
    imagesList = []
    xpathIds = frames.get_xpath_ids()

    RoboVietstockList = []

    if int(config('IS_ROBO_CHART')) > 0 and int(config('LOGIN_ROBO')) > 0:
        for xpath in xpathIds:
            tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_SUM_FA_2_{xpath}.png")
            if os.path.isfile(tmpPath):
                tmpImagePath = Image.open(tmpPath)
                RoboVietstockList.append(tmpImagePath)

        if int(config('IS_CANSLIM')) > 0:
            canSlimPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_CAN_SLIM.png")
            if os.path.isfile(canSlimPath):
                RoboVietstockList.append(Image.open(canSlimPath))

        if int(config('IS_STOCK_RATING')) > 0:
            stockRatingCodePath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_STOCK_RATING.png")
            if os.path.isfile(stockRatingCodePath):
                RoboVietstockList.append(Image.open(stockRatingCodePath))

    if int(config('IS_VIETSTOCK_CHART')) > 0 and int(config('LOGIN_VIETSTOCK')) > 0:
        vietstockChartCodePath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_VIETSTOCK_CHART.png")
        if os.path.isfile(vietstockChartCodePath):
            RoboVietstockList.append(Image.open(vietstockChartCodePath))

    if len(RoboVietstockList) > 0:
        rbvt_image = images.get_concat_v_multi_resize(RoboVietstockList)
        rbvt_path = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_rbvt.png")
        rbvt_image.save(rbvt_path)
        imagesList.append(rbvt_path)
        logging.info(f"Saved rbvt: {rbvt_path}")

    if int(config('LOGIN_WICHART')) > 0:

        if int(config('IS_WICHART_12CHARTS')) > 0:
            wichart_imgs = []
            idx = 0
            wiChartMainPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_FA_8.png")
            try:
                while True:
                    wiChartCodePath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_FA_8_{idx}.png")
                    if os.path.exists(wiChartCodePath):
                        wichart_imgs.append(Image.open(wiChartCodePath))
                        idx += 1
                    else: break

                if len(wichart_imgs) > 0:
                    wiChart = images.concat_images_horizontally(wichart_imgs)
                    logging.info(f"WiChart: {wiChart}")
                    if wiChart:
                        wiChart.save(wiChartMainPath)
                        logging.info(f"Saved WiChart: {wiChartMainPath}")
                        imagesList.append(wiChartMainPath)
            except: pass
        
        if int(config('IS_WICHART_ANALYSIS')) > 0:

            wiChart_report_path = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_WICHART_ANALYSIS_REPORT.png")

            if os.path.exists(wiChart_report_path):
                imagesList.append(wiChart_report_path)
                logging.info(f"Saved WiChart Report: {wiChart_report_path}")

    if int(config('IS_ROBO_CHART')) > 0 and int(config('LOGIN_ROBO')) > 0:
        for xpath in xpathIds:
            tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_SUM_FA_2_{xpath}.png")
            remove_file(tmpPath)

        if int(config('IS_CANSLIM')) > 0:
            remove_file(canSlimPath)

        if int(config('IS_STOCK_RATING')) > 0:
            remove_file(stockRatingCodePath)
    
    if int(config('IS_VIETSTOCK_CHART')) > 0 and int(config('LOGIN_VIETSTOCK')) > 0:
        remove_file(vietstockChartCodePath)

    if int(config('LOGIN_WICHART')) > 0:
        if int(config('IS_WICHART_12CHARTS')) > 0:
            idx = 0
            try:
                while True:
                    wiChartCodePath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_FA_8_{idx}.png")
                    if os.path.exists(wiChartCodePath):
                        remove_file(wiChartCodePath)
                        idx += 1
                    else: break

            # wiChart_report_path = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"{stockCode}_ANALYSIS_REPORT.png")
            # if os.path.exists(wiChart_report_path):
            #     remove_file(wiChart_report_path)

            except: pass

    thisSessionImages = move_files()
    logging.info(f"Saved: {thisSessionImages}")

    if returnImage: return thisSessionImages
    return None

def remove_files(path):
    [f.unlink() for f in Path(path).glob("*") if f.is_file()]

def remove_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except: pass

def move_files() -> list[str]:
    source_dir = config('TMP_SAVE_IMAGES_PATH')
    target_dir = config('SAVE_IMAGES_PATH')

    file_names = os.listdir(source_dir)

    thisSessionImages = []

    for file_name in file_names:
        oldLoc = os.path.join(source_dir, file_name)
        newLoc = os.path.join(target_dir, file_name)
        shutil.move(oldLoc, newLoc)
        thisSessionImages.append(newLoc)

    return thisSessionImages

def removeSocialContacts(driver: webdriver.Chrome):
    try:
        driver.execute_script("var containers = document.getElementsByClassName('mmt-container'); if (containers) containers[0].remove();")
    except:
        pass

def customScreenshot(driver: webdriver.Chrome, xpath: str):
    try:
        tmpPath = os.path.join(config('TMP_SAVE_IMAGES_PATH'), f"TEST.png")
        ele = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        save_element_screenshot(driver, tmpPath, xpath, ele)
    except:
        pass