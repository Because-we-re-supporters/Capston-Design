import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

def todaySTR():
    today = str(datetime.today().year)
    if len(str(datetime.today().month))<2:
        today += str(0)+str(datetime.today().month)
    else :
        today += str(datetime.today().month)
    if len(str(datetime.today().day))<2:
        today += str(0)+str(datetime.today().day)
    else :
        today += str(datetime.today().day)
    return today

def makeDir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def saveData(data, name, flag):
    src = "static/data/modelInput"
    makeDir(src)
    data.to_csv(src + name + '.csv', encoding='utf-8', index=flag)
    print("Data saving is complete!")

def parseToday():
    if datetime.now().hour>18:
        return True
    elif datetime.now().hour==18 and datetime.now().minute>=4:
        return True
    else:
        return False

#코스피 투자자별 매매동향 1page 10개
def KOSPIInvestor():
    if parseToday():
        end=7
    else:
        end=8
    for i in range(1, end):
        url = "https://finance.naver.com//sise/investorDealTrendDay.nhn?bizdate=" + todaySTR() + "&sosok=01&page=" + str(i)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        # Trade Trends
        data = soup.select('table', attrs={"summary": "시간별 순매수에 관한 표 입니다."})
        data = str(data)
        data = re.sub('<.+?>', '', data, 0).strip()
        data = data.replace('\n', ' ')
        data = data.replace('[', ' ')
        data = data.replace(']', ' ')
        data = data.replace(',', '')
        data = data.replace('21.', '2021-')
        data = data.replace('.', '-')
        data = data.split(' ')
        data = [v for v in data if v]
        # print(data[:14])
        start = 14
        if i==1 and not parseToday():
            start=14+11
        for j in range(start, 14 + 11 * 10, 11):
            if i == 1 and j == start:
                d = pd.DataFrame(data[j:j + 11]).T
            else:
                d = pd.concat([d, pd.DataFrame(data[j:j + 11]).T], axis=0)
    header = ['일자', '개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융기관', '연기금 등', '기타법인']
    d.columns = header
    d=d[['일자','기관','개인','외국인','연기금 등']]
    d[['기관','개인','외국인','연기금 등']]=d[['기관','개인','외국인','연기금 등']].apply(pd.to_numeric)
    for col in d.columns:
        if col=='일자': continue
        d[col]*=100
    d=d[::-1]
    d=d.reset_index(drop=True)
    return d

#코스닥 투자자별 매매동향
def KOSDAQInvestor():
    if parseToday():
        end=7
    else:
        end=8
    for i in range(1, end):
        url = "https://finance.naver.com//sise/investorDealTrendDay.nhn?bizdate=" + todaySTR() + "&sosok=02&page=" + str(i)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        # Trade Trends
        data = soup.select('table', attrs={"summary": "시간별 순매수에 관한 표 입니다."})
        data = str(data)
        data = re.sub('<.+?>', '', data, 0).strip()
        data = data.replace('\n', ' ')
        data = data.replace('[', ' ')
        data = data.replace(']', ' ')
        data = data.replace(',', '')
        data = data.replace('21.', '2021-')
        data = data.replace('.', '-')
        data = data.split(' ')
        data = [v for v in data if v]
        # print(data[:14])
        start = 14
        if i==1 and not parseToday():
            start=14+11
        for j in range(start, 14 + 11 * 10, 11):
            if i == 1 and j == start:
                d = pd.DataFrame(data[j:j + 11]).T
            else:
                d = pd.concat([d, pd.DataFrame(data[j:j + 11]).T], axis=0)
    header = ['일자', '개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융기관', '연기금 등', '기타법인']
    d.columns = header
    d=d[['일자','기관','개인','외국인','연기금 등']]
    d[['기관','개인','외국인','연기금 등']]=d[['기관','개인','외국인','연기금 등']].apply(pd.to_numeric)
    for col in d.columns:
        if col=='일자': continue
        d[col]*=100
    d=d[::-1]
    d=d.reset_index(drop=True)
    return d

#model input
def KOSPIinput():
    df2=KOSPIInvestor()
    if len(df1)<len(df2):
        data=pd.concat([df1[-len(df1):],df2[-len(df1):]], axis=1)
    else:
        data=pd.concat([df1[-len(df2):],df2[-len(df2):]], axis=1)
    data = data[['일자', '지수', '대비', '기관', '외국인','개인', '연기금 등']]
    print("KOSPI data input")
    return data

def KOSDAQinput():
    df1=KOSDAQprices()
    df2=KOSDAQInvestor()
    if len(df1)<len(df2):
        data=pd.concat([df1[-len(df1):],df2[-len(df1):]], axis=1)
    else:
        data=pd.concat([df1[-len(df2):],df2[-len(df2):]], axis=1)
    data=data[['일자','지수','대비','기관','외국인','개인','연기금 등']]
    print("KOSDAQ data input")
    return data