import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
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

#코스피
def KOSPI():
    # 9시 ~ 18시 4분까지 실시간 크롤링 -> 그 외는 저장된 데이터 불러오기
    url = "https://finance.naver.com//sise/investorDealTrendDay.nhn?bizdate="+todaySTR()+"&sosok=01"
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
    res=requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    #Trade Trends
    data=soup.select('table', attrs={"summary": "시간별 순매수에 관한 표 입니다."})
    data=str(data)
    data=re.sub('<.+?>', '', data, 0).strip()
    data=data.replace('\n',' ')
    data=data.replace('[',' ')
    data=data.replace(']',' ')
    data=data.replace(',',' ')
    data=data.split(' ')
    data=[v for v in data if v]
    header=['개인', '외국인', '기관계','금융투자', '보험', '투신(사모)', '은행', '기타금융기관', '연기금등','기타법인']
    df=pd.DataFrame(data[15:25]).T
    df.columns=header
    df[header]=df[header].apply(pd.to_numeric)
    df*=100
    print(df)
    return df

def KOSDAQ():
    #코스닥
    # 9시 ~ 18시 4분까지 실시간 크롤링 -> 그 외는 저장된 데이터 불러오기
    url = "https://finance.naver.com//sise/investorDealTrendDay.nhn?bizdate="+todaySTR()+"&sosok=02"
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
    res=requests.get(url,headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')

    #Trade Trends
    data=soup.select('table', attrs={"summary": "시간별 순매수에 관한 표 입니다."})
    data=str(data)
    data=re.sub('<.+?>', '', data, 0).strip()
    data=data.replace('\n',' ')
    data=data.replace('[',' ')
    data=data.replace(']',' ')
    data=data.replace(',',' ')
    data=data.split(' ')
    data=[v for v in data if v]
    header=['개인', '외국인', '기관계','금융투자', '보험', '투신(사모)', '은행', '기타금융기관', '연기금등','기타법인']
    df=pd.DataFrame(data[15:25]).T
    df.columns=header
    df[header]=df[header].apply(pd.to_numeric)
    df*=100
    print(df)
    return df
KOSDAQ()
KOSPI()