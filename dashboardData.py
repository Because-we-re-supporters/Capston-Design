from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import numpy as np
import urllib.request as req

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}

urls = [
        "https://finance.naver.com/",
        "http://finance.naver.com/marketindex/",
        "https://finance.naver.com/sise/sise_market_sum.nhn?page=1",
        "http://finance.naver.com/marketindex/?tabSel=materials#tab_section",
        "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B8%B0%EC%A4%80%EA%B8%88%EB%A6%AC&oquery=%EA%B8%B0%EC%A4%80%EA%B8%88%EB%A6%AC&tqi=h5XaswprvhGssC1GbbVssssssUl-523857"
    ]

def saveData(data, name, flag):
    src = "static/data/dashboard/"
    data.to_csv(src + name + '.txt', encoding='utf-8', sep=';', index=flag)
    print("Data saving is complete!")
def removeTag(x):
    x = str(x)
    x = re.sub('<.+?>', '', x, 0).strip()
    x = x.replace('[', '')
    x = x.replace(']', '')
    return x
def urlOpen(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

def chart(soup):
    print(os.getcwd())
    name = ['KOSPI', 'KOSDAQ', 'KOSPI200']
    src = "static/data/dashboard/"
    # print(os.listdir(src))
    data = soup.find_all("img")
    count = 0
    for img in data:
        img_url = img["src"]
        print(count, ".", img_url)
        if 'chart' in str(img_url):
            req.urlretrieve(img_url, src + name[count] + ".jpg")
            count += 1

    data = soup.find_all("div", attrs={"class": "dsc_area"})
    data = str(data)
    data = re.sub('<.+?>', '', data, 0).strip()
    data = data.replace('\n', ' ')
    data = data.replace('[', ' ')
    data = data.replace('+', ' ')
    data = data.replace(']', ' ')
    data = data.split(' ')

    data = [v for v in data if v]
    trans = []
    for i in range(len(data)):
        if data[i] == '개인' or data[i] == '외국인' or data[i] == '기관':
            trans.append(data[i + 1])

    data = soup.find_all("div", attrs={"class": "heading_area"})
    data = str(data)
    data = re.sub('<.+?>', '', data, 0).strip()
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.replace(', ', '')
    data = data.replace('\n', ' ')
    data = data.split(' ')
    data = [v for v in data if v]
    for i in range(2):
        for i in range(0, len(data), 5):
            if i < 5:
                da = pd.DataFrame(data[i:i + 5]).T
            else:
                da = pd.concat([da, pd.DataFrame(data[i:i + 5]).T])
        da['개인'] = [0, 0, 0]
        da['외국인'] = [0, 0, 0]
        da['기관'] = [0, 0, 0]
        da = da.reset_index(drop=True)
        for i in range(len(da[0])):
            if (da[0][i] == '코스피200'):
                da['개인'][i] = trans[6]
                da['외국인'][i] = trans[7]
                da['기관'][i] = trans[8]
            if (da[0][i] == '코스피'):
                da['개인'][i] = trans[0]
                da['외국인'][i] = trans[1]
                da['기관'][i] = trans[2]
            if (da[0][i] == '코스닥'):
                da['개인'][i] = trans[3]
                da['외국인'][i] = trans[4]
                da['기관'][i] = trans[5]

        checkArr = ['코스피200', '코스피', '코스닥']

        if da[0][0] in checkArr:
            checkArr.remove(da[0][0])
            # print(da[0][0])
        if da[0][1] in checkArr:
            checkArr.remove(da[0][1])
            # print(da[0][1])
        if da[0][2] in checkArr:
            checkArr.remove(da[0][2])
            # print(da[0][2])
        if not checkArr:
            print("arr is empty")
            saveData(da, "chart", False)
            print("dataSave!")
            break
    return
def exchangeAndGold(soup):
    nation=soup.select('h3.h_lst > span.blind')
    nation=removeTag(nation)
    nation=nation.split(', ')
    nation=pd.DataFrame(nation)

    price = soup.select('span.value')
    price=removeTag(price)
    price=price.split(', ')
    price=pd.DataFrame(price)

    change = soup.select('span.change')
    change=removeTag(change)
    change=change.split(', ')
    change=pd.DataFrame(change)

    upDown = soup.select('div.head_info > span.blind')
    upDown=removeTag(upDown)
    upDown=upDown.split(', ')
    upDown=pd.DataFrame(upDown)

    data=pd.concat([nation,price,change,upDown],axis=1)
    data.columns=['국가','가격','변동폭','상승/하강']
    saveData(data.iloc[:4,:],"exchangeRate",False)
    saveData(data.iloc[4:8,:],"nationMarketRate",False)
    saveData(data.iloc[8:,:],"goldOil",False)
    return
def market_capitalization(soup):
    stock_head = soup.find("thead").find_all("th")
    data_head = [head.get_text() for head in stock_head]

    stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
    stock_ = []

    for stock in stock_list:
        if len(stock) > 1:
            stock_.append(stock.get_text().split())

    stock_ = pd.DataFrame(stock_)
    stock_.columns = ['N', '종목명', '현재가', '전일비', '등락률', '액면가', '시가총액', '상장주식수', '외국인비율', '거래량', 'PER', 'ROE']
    stock_.set_index(['N'], inplace=True, drop=True)
    stock_ = stock_.replace('N/A', 0)

    for col in stock_.columns:
        if col == "종목명":
            continue
        if col == "등락률":
            stock_[col] = stock_[col].str.replace('%', '')
            stock_[col] = stock_[col].str.replace('+', '')

        if col == "등락률" or col == "외국인비율" or col == "PER" or col == "ROE":
            # stock_=stock_.astype({col:str})
            # stock_[col]=stock_[col].apply(remove_comma)
            stock_ = stock_.astype({col: np.float32})

    pd.options.display.float_format = '{:.2f}'.format

    saveData(stock_, 'market_capitalization', True)
    return
def material(soup):
    data = soup.find_all("table", attrs={"class": "tbl_exchange"})
    data=str(data)
    data=data.replace('<img alt="상승"','상승 <img alt="상승"')
    data=data.replace('<img alt="하락"','하락 <img alt="하락"')
    data=data.replace('<img alt="보합"','보합 <img alt="보합"')
    data=re.sub('<.+?>', '', data, 0).strip()
    data=data.replace('\n',' ')
    data=data.replace('\t',' ')
    data=data.replace('[','')
    data=data.replace(']','')
    data=data.split(' ')
    d=[]

    for i in data:
        if len(i)>0:
            if(i==','):
                continue
            d.append(i)


    print(d[0]+' '+d[1])
    head1 = d[2:10]
    head1.insert(4,'등락')
    dat=[]
    for i in range(10,10+9*3,9):
        da = d[i : i+9]
        da=pd.DataFrame(da)
        dat.append(da.T)
    data1=pd.concat([dat[0],dat[1],dat[2]])
    data1.columns=head1

    print(d[37]+' '+d[38])
    head2 = d[38:38+7]
    head2.insert(3,'등락')
    dat=[]
    for i in range(45,45+7*6,8):
        da = d[i : i+8]
        da=pd.DataFrame(da)
        dat.append(da.T)
    data2=pd.concat([dat[0],dat[1],dat[2],dat[3],dat[4],dat[5]])
    data2.columns=head2

    print(d[93]+' '+d[94])
    head3 = d[95:95+8]
    head3.insert(4,'등락')
    dat=[]
    for i in range(95+8,95+8+9*11,9):
        da = d[i : i+9]
        da=pd.DataFrame(da)
        dat.append(da.T)

    data3=pd.concat([dat[0],dat[1]])
    for i in range(2,11):
        data3=pd.concat([data3,dat[i]])
    data3.columns=head3


    saveData(data1,"energy",False)
    saveData(data2,"nonMetal",False)
    saveData(data3,"crops",False)
    return
def rate(soup):
    data = soup.select('div._panel_wrapper')
    data = removeTag(data)
    data = data.replace('- ', '0 보합')
    data = data.replace('상승', ' 상승')
    data = data.replace('하락', ' 하락')
    data = data.replace('월 ', '월')
    data = data.replace('사우디아라비아 ', '사우디아라비아')
    data = data.split(' ')
    data = [v for v in data if v]

    rate_data = pd.DataFrame(columns=range(5))
    for i in range(0, len(data), 5):
        if i == 0:
            rate_data = pd.DataFrame(data[i:i + 5]).T
        else:
            rate_data = pd.concat([rate_data, pd.DataFrame(data[i:i + 5]).T])

    rate_data.columns = ['국가', '날짜', '변동폭', '변동량', '상승/하강']
    rate_data = rate_data.reset_index(drop=True)
    saveData(rate_data, "rate", False)
    return
def world(soup):
    w_head=soup.select('div.aside_area > table > thead')[0]
    w_head=str(w_head)
    w_head=re.sub('<.+?>', '', w_head, 0).strip()
    w_head=w_head.replace('[','')
    w_head=w_head.replace(']','')
    w_head=w_head.replace("'",' ')
    w_head=w_head.replace('"',' ')
    w_head=w_head.replace(', ','')
    w_head=w_head.replace('\n',' ')
    w_head=w_head.split(' ')

    w_head=[v for v in w_head if v]
    w_head.insert(2,'등락')


    w_data=soup.select('div.aside_area > table > tbody')[0]
    w_data=str(w_data)
    w_data=re.sub('<.+?>', '', w_data, 0).strip()
    w_data=w_data.replace('[','')
    w_data=w_data.replace(']','')
    w_data=w_data.replace(', ','')
    w_data=w_data.replace('\n',' ')
    w_data=w_data.split(' ')

    w_data=[v for v in w_data if v]
    world_data = pd.DataFrame(columns=range(4))
    for i in range(4,len(w_data),4):
        if i==4:
            world_data = pd.DataFrame(w_data[i:i+4]).T
        else:
            world_data=pd.concat([world_data, pd.DataFrame(w_data[i:i+4]).T ])
    world_data.columns = w_head
    world_data=world_data.reset_index(drop=True)
    saveData(world_data,"world",False)
    return
def updateDashData():
    pool = ThreadPoolExecutor(max_workers=5)
    soupList = list(pool.map(urlOpen, urls))
    chart(soupList[0])
    world(soupList[0])
    exchangeAndGold(soupList[1])
    market_capitalization(soupList[2])
    material(soupList[3])
    rate(soupList[4])
    return