url = "https://mops.twse.com.tw/mops/web/t78sb04_q2"


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib
import tqdm
import time
import pandas as pd
from docx import Document
from docx.shared import Inches

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
year = [ str(i) for i in range(93,110,1)]
year
quarter = ["01","02","03","04"]


if __name__ == '__main__':
    total_df = pd.DataFrame(columns=["年份","季","股票代號","股票名稱","持股比率","產業類別","產業持股比率"])
    driver = webdriver.Chrome(executable_path='C:\\Users\\chiaming\\Desktop\\vs\\武漢肺炎專區\\chromedriver.exe',chrome_options=options)
    driver.get(url)
    
    for yyy in year:
        driver.find_element_by_css_selector('#year').clear()
        Year = driver.find_element_by_css_selector('#year')
        Year.send_keys(yyy)
        for qut in quarter:
            WebDriverWait(driver, 10).until(lambda d: d.find_element_by_css_selector('#season')).click()
            WebDriverWait(driver, 10).until(lambda d: d.find_element_by_css_selector('#season option[value='+"\""+qut+"\""+']')).click()
            WebDriverWait(driver, 10).until(lambda d: d.find_element_by_css_selector('.search input[type="button"]')).click()
            
            time.sleep(5)
            try:
                table = BeautifulSoup(WebDriverWait(driver, 20).until(lambda d: d.page_source),'lxml')
            except:
                time.sleep(10)
                table = BeautifulSoup(WebDriverWait(driver, 20).until(lambda d: d.page_source),'lxml')
                
            table = table.select('table:nth-of-type(2)')[0]
            Y = []
            Quar = []
            Code = []
            Company = []
            Ratio = []
            Industry = []
            IRtio = []
            for i in table.select('.even'):
                try:
                    code = i.select('td:nth-of-type(1)')[0].text
                    company = i.select('td:nth-of-type(2)')[0].text
                    ratio = i.select('td:nth-of-type(3)')[0].text
                    industry = i.select('td:nth-of-type(4)')[0].text
                    Iratio = i.select('td:nth-of-type(5)')[0].text
                    Y.append(yyy)
                    Quar.append(qut)
                    Code.append(code)
                    Company.append(company)
                    Ratio.append(ratio)
                    Industry.append(industry)
                    IRtio.append(Iratio)
                except:
                    continue
            
            new = {"年份":Y,"季":Quar,"股票代號":Code,"股票名稱":Company,"持股比率":Ratio,"產業類別":Industry,"產業持股比率":IRtio}
            new = pd.DataFrame(new)
            print(new.head(3))
            total_df = pd.concat([total_df,new],ignore_index=True)
            
            Y = []
            Quar = []
            Code = []
            Company = []
            Ratio = []
            Industry = []
            IRtio = []
            for i in table.select('.odd'):
                try:
                    code = i.select('td:nth-of-type(1)')[0].text
                    company = i.select('td:nth-of-type(2)')[0].text
                    ratio = i.select('td:nth-of-type(3)')[0].text
                    industry = i.select('td:nth-of-type(4)')[0].text
                    Iratio = i.select('td:nth-of-type(5)')[0].text
                    Y.append(yyy)
                    Quar.append(qut)
                    Code.append(code)
                    Company.append(company)
                    Ratio.append(ratio)
                    Industry.append(industry)
                    IRtio.append(Iratio)
                except:
                    continue
                
            new = {"年份":Y,"季":Quar,"股票代號":Code,"股票名稱":Company,"持股比率":Ratio,"產業類別":Industry,"產業持股比率":IRtio}
            new = pd.DataFrame(new)
            print(new.head(3))
            total_df = pd.concat([total_df,new],ignore_index=True)

total_df.to_csv('0050持股比率.csv',encoding='utf_8_sig',index=False)


top_20 = pd.DataFrame(columns=["年份","季","股票代號","股票名稱","持股比率","產業類別","產業持股比率"])
for y in year:
    for qu in quarter:
        small = total_df[(total_df['年份']==y) & (total_df['季']==qu) ].sort_values('持股比率',ascending=False)[:17]
        top_20 = pd.concat([top_20,small],ignore_index=True)
top_20

len(list(set(top_20.股票代號)))
top_20.持股比率 = [float(i.replace('%','')) for i in top_20.持股比率.values]
top_20.iloc[:50,:].sort_values('持股比率',ascending=False)
25930000*295.5/100000000
top_20[top_20['股票代號']=='3673'].iloc[0,:]
list(set(top_20.股票代號))

import os
os.getcwd()
df = pd.read_csv('市值最高//data.csv',engine='python',sep=',')
df.fillna(0,inplace=True)
df
name = []
df
for i in df.columns.values[2:]:
    df[i] = [int(str(l).replace(',',''))/100 for l in df[i].values]
    for k in df.sort_values(i,ascending=False)[:15].企業名稱.values:
        name.append(k)
list(set(name))

df[df.企業名稱=='台灣大']
df


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path='C:\\Users\\chiaming\\Desktop\\vs\\武漢肺炎專區\\chromedriver.exe')
driver.get("http://www.baidu.com")
time.sleep(3)
print(driver.current_window_handle) #打印當前窗口的句柄
print(driver.title) #打印當前頁面標題
driver.window_handles
driver.switch_to_window(driver.window_handles[-1])
#通過執行js語句爲元素添加target="_blank"屬性
js = 'document.getElementsByName("tj_trnews")[0].target="_blank"'
driver.execute_script(js)

news = driver.find_element_by_name('tj_trnews')
news.click()
time.sleep(3)

handles = driver.window_handles #獲取當前打開的所有窗口的句柄
print(handles)

driver.switch_to.window(handles[1]) #切換到第二個窗口的句柄
print(driver.current_window_handle)
print(driver.title)

driver.switch_to.window(handles[0]) #切換回主頁句柄
print(driver.title)


