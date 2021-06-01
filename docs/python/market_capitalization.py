import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
from datetime import datetime
import urllib.request as req
import re
from func import *

url = "https://finance.naver.com/sise/sise_market_sum.nhn?page=1"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'lxml')

stock_head = soup.find("thead").find_all("th")
data_head = [head.get_text() for head in stock_head]

stock_list = soup.find("table", attrs={"class": "type_2"}).find("tbody").find_all("tr")
stock_=[]

for stock in stock_list:
    if len(stock)>1:
        stock_.append(stock.get_text().split())
        
stock_ = pd.DataFrame(stock_)
stock_.columns=['N', '종목명', '현재가', '전일비', '등락률', '액면가', '시가총액', '상장주식수', '외국인비율', '거래량', 'PER', 'ROE']
stock_.set_index(['N'],inplace = True, drop=True)
stock_=stock_.replace('N/A',0)

print(stock_.dtypes)
for col in stock_.columns:
    if col == "종목명":
        continue
    if col == "등락률":
        stock_[col]=stock_[col].str.replace('%','')
        stock_[col]=stock_[col].str.replace('+','')
    
    
    if col=="등락률" or col == "외국인비율" or col=="PER" or col=="ROE":
        #stock_=stock_.astype({col:str})
        #stock_[col]=stock_[col].apply(remove_comma)
        stock_=stock_.astype({col:np.float32})
            
pd.options.display.float_format = '{:.2f}'.format

saveData(stock_,'market_capitalization',True)
