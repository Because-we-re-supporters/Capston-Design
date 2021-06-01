import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import os
from datetime import datetime
import urllib.request as req
import re

from func import *

url = "http://finance.naver.com/marketindex/?tabSel=materials#tab_section"
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
res=requests.get(url,headers=headers)
soup = BeautifulSoup(res.text, 'lxml')


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
print(data1)
print(data2)
print(data3)