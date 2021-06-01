import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import os
from datetime import datetime
import urllib.request as req
import re

from func import *

url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B8%B0%EC%A4%80%EA%B8%88%EB%A6%AC&oquery=%EA%B8%B0%EC%A4%80%EA%B8%88%EB%A6%AC&tqi=h5XaswprvhGssC1GbbVssssssUl-523857"
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
res=requests.get(url,headers=headers)
soup = BeautifulSoup(res.text, 'lxml')

r_data=soup.select('div._panel_wrapper')
r_data=removeTag(r_data)
r_data=r_data.replace('- ','0 보합')
r_data=r_data.replace('상승',' 상승')
r_data=r_data.replace('하락',' 하락')
r_data=r_data.replace('월 ','월')
r_data=r_data.replace('사우디아라비아 ','사우디아라비아')
r_data=r_data.split(' ')
r_data=[v for v in r_data if v]
#r_data

rate_data = pd.DataFrame(columns=range(5))
for i in range(0,len(r_data),5):
    if i==0:
         rate_data = pd.DataFrame(r_data[i:i+5]).T
    else:
        rate_data=pd.concat([rate_data, pd.DataFrame(r_data[i:i+5]).T ])
        
rate_data.columns = ['국가','날짜','변동폭','변동량','상승/하강']
rate_data=rate_data.reset_index(drop=True)
saveData(rate_data,"rate",False)
