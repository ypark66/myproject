import re
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.select import Select
import smtplib
from email.mime.text import MIMEText
def error_check(driver):
    if driver.current_url == 'https://apps.uillinois.edu/selfservice/error/':
        return False
    else:
        return True
username='ypark66'
password='shibalPW12!'



driver = webdriver.Firefox(executable_path=r'C:\Users\fasoo-03\gecko\geckodriver.exe')
driver.manage().timeouts().implicitlyWait()
print('Browser opened')
ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
driver.switch_to.window(driver.window_handles[-1])
driver.get('https://apps.uillinois.edu/selfservice/error/')
ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
driver.switch_to.window(driver.window_handles[-1])
driver.get('https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior')
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[1])
driver.get('https://www.naver.com/')
#print('third tab added')
#print(driver.window_handles)
#driver.switch_to.window(driver.window_handles[-1])
#print('window switched to new tab')
#print(driver.window_handles)
#driver.get('https://apps.uillinois.edu/selfservice/')
#driver.switch_to.window(driver.window_handles[0])
#driver.get('https://www.naver.com')
#driver.switch_to.window(driver.window_handles[1])
#driver.get('https://www.naver.com')
#driver.switch_to.window(driver.window_handles[2])
#driver.get('https://www.naver.com')



