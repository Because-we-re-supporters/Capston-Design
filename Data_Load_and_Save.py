import time
import os
import pandas as pd
import numpy as np
from static.libs.inverstingCrawling import *
from static.libs.crawling_top20 import *
from static.libs.feature_extraction import *

name, data = makeModelInput()

if name[0] == 'kosdaq':
    kosdaq_invest = data[0]
    kospi_invest = data[1]
elif name[0] == 'kospi':
    kospi_invest = data[0]
    kosdaq_invest = data[1]
    
kospi_invest['일자'] = pd.to_datetime(kospi_invest['일자'])
kospi_invest = kospi_invest.set_index('일자')
kosdaq_invest['일자'] = pd.to_datetime(kosdaq_invest['일자'])
kosdaq_invest = kosdaq_invest.set_index('일자')

invest_columns = ['기관', '외국인', '개인', '기타', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '한국금리', '천연가스', '미국금리', '다우존스', '나스닥', '구리', 'WTI']
kospi_invest = kospi_invest[invest_columns]
kosdaq_invest = kosdaq_invest[invest_columns]

kospi_name, kospi_list = getStock('kospi')
kosdaq_name, kosdaq_list = getStock('kosdaq')

kospi_df = {}
for name, kospi in zip(kospi_name, kospi_list):
    df = kospi[['일자', '종가', '시가', '고가', '저가', '거래량']].copy()
    df = df[:61]
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.set_index('일자')
    df = df.sort_index()
    df = df.astype('float64')
    df['대비'] = df['종가'].diff()
    df['대비%'] = round(df['대비'] / df['종가'] * 100, 2)
    df.columns = ['close', 'open', 'high', 'low', 'volume', '대비', '대비%']
    df = df[1:]
    kospi_df[name] = df

kosdaq_df = {}
for name, kosdaq in zip(kosdaq_name, kosdaq_list):
    df = kosdaq[['일자', '종가', '시가', '고가', '저가', '거래량']].copy()
    df = df[:61]
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.set_index('일자')
    df = df.sort_index()
    df = df.astype('float64')
    df['대비'] = df['종가'].diff()
    df['대비%'] = round(df['대비'] / df['종가'] * 100, 2)
    df.columns = ['close', 'open', 'high', 'low', 'volume', '대비', '대비%']
    df = df[1:]
    kosdaq_df[name] = df

column_sort = ['close', '대비', '기관', '외국인', '개인', '기타', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', 'open', 'high', 'low', 'volume', '대비%', '한국금리', '천연가스', '미국금리', '다우존스', '나스닥', '구리', 'WTI']
res_kospi = {}
for key, df in kospi_df.items():
    df = pd.merge(df, kospi_invest, on='일자')
    df = df[column_sort]
    res_kospi[key] = df

res_kosdaq = {}
for key, df in kosdaq_df.items():
    df = pd.merge(df, kosdaq_invest, on='일자')
    df = df[column_sort]
    res_kosdaq[key] = df

path = 'static/data/kospi/'
for key, df in res_kospi.items():
    df.to_csv(path + key + '.csv', encoding='utf-8-sig')
    
path = 'static/data/kosdaq/'
for key, df in res_kosdaq.items():
    df.to_csv(path + key + '.csv', encoding='utf-8-sig')

path = 'static/data/kospi/'
for file in os.listdir(path):
    df = pd.read_csv(path + file)
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.set_index('일자')
    df.index.name = '일자'
    df = Feature_Extraction(df)
    df.replace([np.inf, -np.inf], 0, inplace = True)
    df = df.drop(['TRIX'], axis = 1)
    df.to_csv(path + file, encoding='utf-8-sig')

path = 'static/data/kosdaq/'
for file in os.listdir(path):
    df = pd.read_csv(path + file)
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.set_index('일자')
    df.index.name = '일자'
    df = Feature_Extraction(df)
    df.replace([np.inf, -np.inf], 0, inplace = True)
    df = df.drop(['TRIX'], axis = 1)
    df.to_csv(path + file, encoding='utf-8-sig')

print('finish')