import logging, coloredlogs
import requests
import subprocess

from selenium import webdriver

coloredlogs.install()
port = 2025

def initBrowser():
    try:
        logging.info('Connect to existing chrome driver')
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless=new")
        options.debugger_address = f'127.0.0.1:{port}'
        driver = webdriver.Chrome(options=options)

        return driver
    except Exception as e:
        logging.error(f"[initBrowser] {e}")
        exit()

def is_chrome_running_on_port(port):
    try:
        requests.get(f"http://localhost:{port}", timeout=5)
        return True
    except:
        return False
    
def start_browserViaCMD():
    global port
    # cmd = f'"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --remote-debugging-port={port}'
    cmd = f'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --profile-directory="Default" --remote-debugging-port={port}'
    subprocess.Popen(cmd, shell=True)

def getBrowser():

    if is_chrome_running_on_port(port):
        print(f"Chrome is running on port {port}.")
        return initBrowser()
    else:
        print(f"Chrome is not running on port {port}.")
        start_browserViaCMD()
        return initBrowser()
