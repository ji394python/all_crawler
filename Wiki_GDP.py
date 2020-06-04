from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import numpy as np
import os 
import time 
import pandas as pd
import urllib
import math
from googletrans import Translator
translate = Translator()
head = 'https://www.wikiwand.com'
driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get("https://www.wikiwand.com/zh-mo/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E7%9C%81%E7%BA%A7%E8%A1%8C%E6%94%BF%E5%8C%BA%E4%BA%BA%E5%9D%87%E5%9C%B0%E5%8C%BA%E7%94%9F%E4%BA%A7%E6%80%BB%E5%80%BC%E5%88%97%E8%A1%A8")
main = WebDriverWait(driver, 10).until(lambda d: d.find_elements_by_css_selector('tr:nth-child(5) ul'))

wiki = BeautifulSoup(driver.page_source,'lxml')
store = dict()
for i in range(31):
    href = wiki.select("tr:nth-child(5) ul > li:nth-of-type("+str(i+1)+") .int-link")[0]['href']
    text = wiki.select("tr:nth-child(5) ul > li:nth-of-type("+str(i+1)+") .int-link")[0].text
    print(f"{[i+1]} "+ text)
    driver.get(head+href)
    time.sleep(3)
    WebDriverWait(driver,20).until(lambda d:d.find_elements_by_css_selector('#section_历年GDP指标 tr:nth-of-type(4) td:nth-of-type(4)'))
    town = BeautifulSoup(driver.page_source,'lxml')
    value = []
    for row in range(35):
        try:
            value.append(town.select('#section_历年GDP指标 tr:nth-of-type('+str(row+4)+') > td:nth-of-type(4)')[0].text)
        except:
            value.append(0)
            f"第幾個{row}開始為空值"
    store[text] = store.get(text,value)
    print(store[text])
df = pd.DataFrame(store)

targer = pd.read_html(driver.current_url)

## 讀進資料與反轉
df = pd.read_excel('GDD資料.xlsx',thousands=',')
df.set_index(df.columns[0],inplace=True)
df = df.T
df = df[df.columns[::-1]]
df.columns = [str(i)+"_1" for i in df.columns.values]

base_df = ''
col_count = 0
multiple = 1
while base_df != '2018_120':
    base_df = df.columns.values[col_count]
    col_count += 1
    next_df = df.columns.values[col_count]
    space = round((df[next_df] - df[base_df])/120,3)
    
    while multiple != 120:
        multiple += 1
        df[base_df[:base_df.find('_')]+'_'+str(multiple)] = df[base_df] + space*multiple
        print (base_df[:base_df.find('_')]+'_'+str(multiple))
    
    base_df = base_df[:base_df.find('_')]+'_'+str(multiple)
    multiple = 1

df.to_excel('[完整資料]各省GDP平滑資料集.xlsx',index=True,header=True,encoding='utf_8_sig')
