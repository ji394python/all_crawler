from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import time
import datetime
import copy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib

### 目標：爬完所有小的圓形國旗
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://www.countryflags.com/en/north-america/')

for i in range(4):
    WebDriverWait(driver, 10).until(lambda d: d.find_element_by_css_selector('#navbar li:nth-child('+str(4+i)+') a')).click()
    url_tentative = driver.current_url
    num_flag = len(WebDriverWait(driver, 10).until(lambda d: d.find_elements_by_css_selector('.layer')))
    for k in range(num_flag):
        WebDriverWait(driver, 10).until(lambda d: d.find_elements_by_css_selector('.layer'))[k].click()
        WebDriverWait(driver, 10).until(lambda d: d.find_element_by_css_selector('.btn-custom-icon .big')).click()
        try:
            WebDriverWait(driver, 10).until(lambda d: d.find_element_by_css_selector('.push-banner:nth-child(11) tr+ tr .text-center+ .text-center .btn-default')).click()
        except:
            print(k)
        driver.get(url_tentative)

f"完成!!!"