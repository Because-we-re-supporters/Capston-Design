import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import os
from datetime import datetime
import urllib.request as req
import re
from concurrent.futures import ThreadPoolExecutor

def parseToday():
    if datetime.today().weekday()==5 or datetime.today().weekday()==6:
        return True
    elif datetime.today().weekday()==0 and datetime.now().hour<9:
        return True
    elif datetime.now().hour>18:
        return True
    elif datetime.now().hour==18 and datetime.now().minute>=4:
        return True
    else:
        return False

def parseTable(url):
    end = 8
    for i in range(1, end):
        link = url + str(i)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
        res = requests.get(link, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        # Trade Trends
        data = soup.select('table', attrs={"class": "type2"})
        data = str(data)
        
        data = re.sub('<.+?>', '', data, 0).strip()
        data = data.replace('\n', ' ')
        data = data.replace('\t', ' ')
        data = data.replace('[', ' ')
        data = data.replace(']', ' ')
        data = data.replace(', ', ' ')
        data = data.replace(',', '')
        data = data.replace('<img alt="하락"', '-<img alt="하락"')
        
        data = data.split(' ')
        data = [v for v in data if v]
    
        start = 7
        if i==1 and not parseToday():
            start=14
        for j in range(start, 7 + 10 * 7, 7):
            if i == 1 and j == start:
                d = pd.DataFrame(data[j:j + 6]).T
            else:
                d = pd.concat([d, pd.DataFrame(data[j:j + 6]).T], axis=0)
    d.columns=['일자','종가','대비','시가','고가','저가']
    #d[['일자', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']]= d[['개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']].apply(pd.to_numeric)
    #d = d[::-1]
    
    print(len(d))
    
    d = d.reset_index(drop=True)
    return d

def parseTable2(url):
    end = 5
    for i in range(1, end):
        link = url + str(i)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
        res = requests.get(link, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        # Trade Trends
        data = soup.select('table', attrs={"summary":"외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다."})
        data = str(data)
        
        data = re.sub('<.+?>', '', data, 0).strip()
        data = data.replace('\n', ' ')
        data = data.replace('\t', ' ')
        data = data.replace('[', ' ')
        data = data.replace(']', ' ')
        data = data.replace(', ', ' ')
        data = data.replace(',', '')
        data = data.replace('<img alt="하락"', '-<img alt="하락"')
        
        data = data.split(' ')
        data = [v for v in data if v]
        start = 68
        if i==1 and not parseToday():
            start=68+9
        for j in range(start, 68 + 9 * 20, 9):
            if i == 1 and j == start:
                d = pd.DataFrame(data[j+3:j + 9]).T
            else:
                d = pd.concat([d, pd.DataFrame(data[j+3:j + 9]).T], axis=0)
                
    d.columns=['등락률','거래량','기관 순매매량','외국인 순매매량','외국인 보유주수','외국인 보유률']
    #d[['일자', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']]= d[['개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']].apply(pd.to_numeric)
    #d = d[::-1]
    
    print(len(d))
    
    d = d.reset_index(drop=True)
    return d

def getStock(flag):
    if flag=='kospi':
        url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0"
    elif flag=='kosdaq':
        url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1"
        
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
    res=requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.find_all("a", attrs={"class": "tltle"})
    urls1=[]
    urls2=[]
    name=[]
    base = 'https://finance.naver.com/'
    for d in data[:20]: #코스피 코스닥 상위 20개만 긁기
        name.append(re.sub('<.+?>', '', str(d), 0).strip())
        code=d["href"].replace('main','sise_day')
        urls1.append(base+code+'&page=')
        code2=d["href"].replace('main','frgn')
        urls2.append(base+code2+'&page=')
    data1=[]
    data2=[]
    data=[]
    for url in urls1:
        data1.append(parseTable(url))
    for url in urls2:
        data2.append(parseTable2(url))
    for i in range(len(name)):
        data.append(pd.concat([data1[i], data2[i]], axis=1))
        print(str(i+1)+'. '+name[i])
        print(data[i])
    
    return name,data