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



colors = ['#2176FF','#33A1FD','#FDCA40','#D1D646','#F97068','#4F3824','#D0E37F','#004643','#7A918D','#A63D40']
import random
import math
plt.rcParams["figure.dpi" ] = 72
next_date = 1
fig = plt.figure(figsize=(16,9))
count_error = 0
next_date = 1
def draw_barchart(data,current_year):
    fig = plt.figure(figsize=(16,9))
    ax1 = fig.add_axes([0,0,1,1])
    ax2 = fig.add_axes([0.08, 0.05, 0.87, 0.85])
    ax2.set_ylim(0,15)
    ab = data.sort_values(current_year,ascending=True)[current_year].tail(16)
    maxValue = max(ab.values)
    ax2.set_xlim(0,maxValue+2000)
    store = [ i for i in range(0,math.floor(maxValue),math.floor(maxValue/5))]

    next_date = globals()['next_date']
    date = int(current_year[current_year.find('_')+1:])
    ### 第一天確認速度、排名
    if((date%30==1)):
        rank = list(ab.index.values)
        if date > 270:
            next_date = 1
            year = 1
        else:
            next_date += 30
            year = 0
        if current_year != '2020/3/31_1':
            ab_30 = data.sort_values( str(int(current_year[:4])+year) +'-'+ current_year[5:current_year.find('_')] +'_'+str(next_date),ascending=False)[str(int(current_year[:4])+year) +'-'+ current_year[5:current_year.find('_')] +'_'+str(next_date)].head(12)
            for i in range(len(ab_30)):
                each_bar[ab_30.index[i]][-2] = ab_30.values[i]
                try:
                    each_bar[ab_30.index[i]][-1] = ab_30.values[i] - ab[ab_30.index[i]]
                except:
                    each_bar[ab_30.index[i]][-1] = 1
        print(str(int(current_year[:4])+year) +'-'+ current_year[5:current_year.find('_')] +'_'+str(next_date))
        for s in range(len(rank)):
            #print('進入')
            each_bar[rank[s]][3] = 0  #本次初始速度
            each_bar[rank[s]][4] = 0
            try:
            #    print('二次')
                each_bar[rank[s]][1] = abs(s-11)  #本次排名
            except:
                each_bar[rank[s]][1] = -1
            try:
            #    print('二次')
            #    print(ab_30.index,rank[s])
                each_bar[rank[s]][2] = abs(list(ab_30.index).index(rank[s]) - 11) #下次排名
            except:
                each_bar[rank[s]][2] = -1
            if abs(s-11) != each_bar[rank[s]][2]:
                each_bar[rank[s]][3]= each_bar[rank[s]][2] - abs(s-11)  #決定本次速度
            else:
                each_bar[rank[s]][3] = 0
                #each_bar[rank[s]][6] = each_bar[rank[s]][5]*fix



    #### 每天畫圖
    world = mpimg.imread('bg.jpg',0)            
    ax1.imshow(world,aspect='auto',alpha=1)
    for i in range(len(ab)):
        value = ab.values[i]
        name = ab.index[i]
        size = check_size(name)
        print(name,i)
        pos_x = size[1]
        zoo = size[0]
        pos = i
        color = colors[random.randint(0,9)]
        if i % 2 ==0:
            adjust = 0
        else:
            adjust = 0
        ax2.add_patch(
            patches.Rectangle(
                (0, pos-1+0.1),   # (x,y)
                value,          # width
                0.8,
                color = color,
                zorder=15
            )
        )
        circle = Ellipse( (value,pos-1+0.5-0.007),400+(1300/(58889.27)*(maxValue-12159.97)),0.785,color=color,alpha=1,zorder=15)
        ax2.add_artist(circle)

        arr_lena1 = caller[name][0][1]
        imagebox1 = OffsetImage(arr_lena1, zoom=zoo/1.7,alpha=1)
        if name =='廣達':
            y_adjust = 0.12
        else:
            y_adjust = 0
        a1 = AnnotationBbox(imagebox1,(-1.5,pos+0.5-1),pad=3,frameon=False,box_alignment=(pos_x+adjust,0.5+y_adjust))
        a1.set_zorder(16)
        '''
        xybox = (value+500,pos)
        a1 = AnnotationBbox(imagebox1,(-0.5,pos+0.3-1),xybox=(-10, 0.),xycoords='data',boxcoords="offset points",pad=3,frameon=False,
        box_alignment=(pos_x+adjust,0.5),bboxprops=dict(edgecolor='#ffffff')
        ,arrowprops=dict(arrowstyle="-",facecolor="#ffffff",color="#ffffff"))
        '''
        ax2.add_artist(a1)

        if value < 7000:
            ax2.text(value+250+70, pos+0.3-2,name+' ',size=16, weight='bold', ha='left', va='center',color='#ffffff',zorder=16,
                bbox=dict(facecolor='#ffffff', alpha=0.2, edgecolor='#646163'))
        else:
            ax2.text(value-30+50, pos+0.3-2,name+' ',size=16, weight='bold', ha='right', va='center',color='#ffffff',zorder=16,
                bbox=dict(facecolor='#000000', alpha=0.2, edgecolor='#646163'))

    ## 圖片區
    # 右上標題

    
    
    #ax1.text(0.75,0.05, '@DT數據趨勢', transform=ax1.transAxes, color='#ffffff', ha='right',size=12,
    #         bbox=dict(facecolor='#938f91', alpha=1,edgecolor='#646163'))  
    ax2.set_zorder(4)
    ax1.set_zorder(3)
    #ax2.patch.set_alpha(1)
    #ax2.xaxis.set_ticks_position('top')
    ax2.set_xticks(store[:-1])
    ax2.tick_params(axis='x', colors='#CECCCC', labelsize=12)
    ax2.set_yticks([])
    ax2.grid(which='major', axis='x', linestyle='-.',zorder=4)
    ax1.axis('off')
    #ax2.axis('off')
    plt.box('off')
    ax2.set_frame_on(False)

def run(current_year):
    globals()['fig'].clear()
    draw_barchart(df,current_year)
    
    
def check_size(name):
    if name == '台積電':
        zoo = 0.12
        pos_x = 1.2
    elif name =='中華電':
        zoo = 0.11
        pos_x = 1.4
    elif name =='國泰金':
        zoo = 0.06
        pos_x = 1.2
    elif name == '聯電':
        zoo = 0.1
        pos_x = 1.1
    elif name =='台塑化':
        zoo = 0.07
        pos_x = 1.1
    elif name =='鴻海':
        zoo = 0.15
        pos_x = 1.35
    elif name=='中鋼':
        zoo = 0.05
        pos_x = 1.55
    elif name == '南亞':
        zoo = 0.07
        pos_x = 1.1
    elif name =='台化':
        zoo = 0.15
        pos_x = 1.1
    elif name == '富邦金':
        zoo = 0.04
        pos_x = 1.55
    elif name=='友達':
        zoo = 0.04
        pos_x = 1.1
    elif name =='兆豐金':
        zoo =0.1
        pos_x = 1.5
    elif name =='台塑':
        zoo = 0.07
        pos_x = 1.1
    elif name =='中鋼':
        zoo = 0.045
        pos_x = 1.2
    elif name == '聯發科':
        zoo = 0.4
        pos_x = 0.95
    elif name =='中信金':
        zoo = 0.67
        pos_x = 0.8
    elif name =='台灣大哥大': 
        zoo = 0.18
        pos_x = 1.03
    elif name =='統一':
        zoo = 0.35
        pos_x = 1.2
    elif name =='大立光':
        zoo = 0.2
        pos_x = 1
    elif name =='華碩':
        zoo=0.08
        pos_x = 1
    elif name =='宏達電':
        zoo=0.12
        pos_x = 1.2
    elif name =='奇美電':
        zoo =0.3
        pos_x=0.85
    elif name =='廣達':
        zoo =0.5
        pos_x =0.95
    elif name =='群創':
        zoo =0.1
        pos_x = 1.1
    elif name=='宏碁':
        zoo=0.15
        pos_x =1.2
    elif name=='台達電':
        zoo=0.45
        pos_x = 1.1
    elif name in ['日月光','日月光控股']:
        zoo=0.15
        pos_x =1.1
    else:
        zoo=0.05
        pos_x=1
    return([zoo,pos_x])