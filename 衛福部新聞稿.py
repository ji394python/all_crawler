
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

content_store = []
month_store = []
day_store = []

driver = webdriver.Chrome(executable_path='chromedriver.exe')
for i in range(1,29,1):
    driver.get('https://www.cdc.gov.tw/Bulletin/List/MmgtpeidAR5Ooai4-fgHzQ?page='+str(i))
    web_html = BeautifulSoup(WebDriverWait(driver, 20).until(lambda d: d.page_source),'lxml')
    for k in range(1,11,1):
        content = web_html.select('.cbp-item:nth-child('+str(k)+') .JQdotdotdot')[0].text
        month = web_html.select('.cbp-item:nth-child('+str(k)+') .icon-year')[0].text
        day = web_html.select('.cbp-item:nth-child('+str(k)+') .icon-date')[0].text
        content_store.append(content)
        month_store.append(month)
        day_store.append(day)

for i in range(len(news)):
    for r in range(3):
        try:
            news.iloc[i,r] = news.iloc[i,r].text
        except:
            continue 
    
news
news = pd.DataFrame({'月':month_store,'日':day_store,'內容':content_store})
news.to_csv('台灣新聞時間資料.csv',encoding='utf_8_sig')

import pandas as pd
new = pd.read_csv('台灣新聞時間資料.csv').iloc[:,1:]
new = new[new.內容.str.contains('國內')]
new.to_csv('台灣新聞資料.csv',encoding='utf_8_sig')
new = pd.read_csv('台灣新聞資料.csv')
new = new.iloc[:,1:]
new['日期']  = [ str(datetime.datetime.strptime('2020-'+str(new.iloc[i,0][3:])+'-'+str(new.iloc[i,1]),'%Y-%b-%d'))[:10] for i in range(len(new))]
new = new.loc[:,['日期','內容']]
new.to_csv('台灣新聞時間資料.csv')