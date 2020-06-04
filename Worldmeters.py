
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

dict_case_total = {}
dict_case_daily = {}
dict_death_total = {}
dict_death_daily = {}
dict_recover_daily = {}

n = 0
dd = ''
dd_store = []
while dd != 'Mar 24':
    v = datetime.datetime.strptime('2020-01-21','%Y-%m-%d') + datetime.timedelta(days=n)
    v = v.strftime('%b %d')
    dd_store.append(v)
    n+=1
    dd = v

## %B 大寫mon %b小寫mon
def find(u):
    return u[u.find('[')+1:u.find(']')].split(',')

def create_dict(store,key):
    store[key] = store.get(key,{})

for i in dd_store:
    text = i.replace('"','')
    create_dict(dict_case_daily,text)
    create_dict(dict_case_total,text)
    create_dict(dict_death_daily,text)
    create_dict(dict_death_total,text)
    create_dict(dict_recover_daily,text)
    

def spider(source,country):
    target = BeautifulSoup(source,'lxml')
    
    date = find(target.text[target.text.find('xAxis'):target.text.find('yAxis')])
    index_date = [i.replace('"','') for i in date]
    
    death_daily_head = target.text.find('data',target.text.find('Daily Deaths'))  #頭
    death_daily_tail = target.text.find('responsive',target.text.find('data',target.text.find('Daily Deaths')))
    death_daily_text = target.text[death_daily_head:death_daily_tail]
    death_daily_value= find(death_daily_text)

    case_total_head = target.text.find('data',target.text.find('Total Cases'))  #頭
    case_total_tail = target.text.find('responsive',target.text.find('data',target.text.find('Total Cases'))) #尾巴
    case_total_text = target.text[case_total_head:case_total_tail]
    case_total_value = find(case_total_text)

    death_total_head = target.text.find('data',target.text.find('Total Deaths')) 
    death_total_tail = target.text.find('responsive',target.text.find('data',target.text.find('Total Deaths'))) #尾巴
    death_total_text = target.text[death_total_head:death_total_tail]
    death_total_value = find(death_total_text)

    cross_head = target.text.find('data',target.text.find('New Cases vs. New Recoveries')+1)  #頭
    cross_tail = target.text.find('responsive',target.text.find('data',target.text.find('New Cases vs. New Recoveries')))
    cross_text = target.text[cross_head:cross_tail]
    recover_daily = cross_text[:cross_text.find('New Case')]
    case_daily = cross_text[cross_text.find('New Case'):]
    recover_value = find(recover_daily)
    case_daily_value = find(case_daily)
    print(index_date)
    for day in range(len(index_date)):
        print(index_date[day],tail,day)
        eval('dict_case_daily')[index_date[day]][tail] = eval('dict_case_daily')[index_date[day]].get(tail,case_daily_value[day])
        eval('dict_case_total')[index_date[day]][tail] = eval('dict_case_total')[index_date[day]].get(tail,case_total_value[day])
        eval('dict_death_daily')[index_date[day]][tail] = eval('dict_death_daily')[index_date[day]].get(tail,death_daily_value[day])
        eval('dict_death_total')[index_date[day]][tail] = eval('dict_death_total')[index_date[day]].get(tail,death_total_value[day])
        try:
            eval('dict_recover_daily')[index_date[day]][tail] = eval('dict_recover_daily')[index_date[day]].get(tail,recover_value[day])
        except:
            continue

### 目標：爬到 總確診、總死亡、每日新增、每日治癒、每日死亡 五點
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://www.worldometers.info/coronavirus/')
store_url =  WebDriverWait(driver, 20).until(lambda d: d.find_elements_by_css_selector('.mt_a'))
store_url = [ i.text.lower() for i in store_url]
for country in store_url:
    tail = country
    if tail == '':
        continue
    else:
        if tail == 'usa':
            driver.get('view-source:https://www.worldometers.info/coronavirus/country/us/')
        elif tail =='s. korea':
            driver.get('view-source:https://www.worldometers.info/coronavirus/country/south-korea/')
        elif tail == 'hong kong':
            driver.get('view-source:https://www.worldometers.info/coronavirus/country/china-hong-kong-sar/')
        else:
            print(tail)
            driver.get('view-source:https://www.worldometers.info/coronavirus/country/'+tail+'/')
    f" 進入{tail} "
    source = WebDriverWait(driver, 20).until(lambda d: d.page_source)
    spider(source,country)
    f"{dict_case_total}"

pd.DataFrame(dict_case_total).to_excel('確診總數.xlsx',index=True,header=True)
pd.DataFrame(dict_case_daily).to_excel('確診每日數.xlsx',index=True,header=True)
pd.DataFrame(dict_death_daily).to_excel('死亡每日數.xlsx',index=True,header=True)
pd.DataFrame(dict_death_total).to_excel('死亡總數.xlsx',index=True,header=True)
pd.DataFrame(dict_recover_daily).to_excel('治癒每日數.xlsx',index=True,header=True)
dict_case_total

