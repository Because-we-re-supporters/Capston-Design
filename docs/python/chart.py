import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import os
from datetime import datetime
import urllib.request as req
import re

from func import *

url = "https://finance.naver.com/"
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.116.15 Safari/537.36'}
res=requests.get(url,headers=headers)
soup = BeautifulSoup(res.text, 'lxml')

name=['KOSPI','KOSDAQ','KOSPI200']


src="C:/Users/tn12q/Documents/Capston-Design/docs/image/"
data = soup.find_all("img")
count = 0
for img in data:
    img_url=img["src"]
    print(count, ".", img_url)
    if 'chart' in str(img_url):
        req.urlretrieve(img_url, src+name[count]+".jpg")
        count+=1
           
            
data = soup.find_all("div", attrs={"class": "dsc_area"})
data=str(data)
data=re.sub('<.+?>', '', data, 0).strip()
data=data.replace('\n',' ')
data=data.replace('[',' ')
data=data.replace('+',' ')
data=data.replace(']',' ')
data=data.split(' ')

data=[v for v in data if v]
trans=[]
for i in range(len(data)):
    if data[i]=='개인' or data[i]=='외국인' or data[i]=='기관':
        trans.append(data[i+1])

data = soup.find_all("div", attrs={"class": "heading_area"})
data=str(data)
data=re.sub('<.+?>', '', data, 0).strip()
data=data.replace('[','')
data=data.replace(']','')
data=data.replace(', ','')
data=data.replace('\n',' ')
data=data.split(' ')
data=[v for v in data if v]

for i in range(2):
    for i in range(0,len(data)):
        #print(data[i])
        if i%5==0:
            if i<5:
                #print(d)
                da=pd.DataFrame(d).T
            else:
                da=pd.concat([da,pd.DataFrame(d).T])
            d=[]
        d.append(data[i])
    da['개인']=[0,0,0]
    da['외국인']=[0,0,0]
    da['기관']=[0,0,0]
    da=da.reset_index(drop=True)
    for i in range(len(da[0])):
        if(da[0][i]=='코스피200'):
            da['개인'][i] = trans[6]
            da['외국인'][i] = trans[7]
            da['기관'][i] = trans[8]
        if(da[0][i]=='코스피'):
            da['개인'][i] = trans[0]
            da['외국인'][i] = trans[1]
            da['기관'][i] = trans[2]
        if(da[0][i]=='코스닥'):
            da['개인'][i] = trans[3]
            da['외국인'][i] = trans[4]
            da['기관'][i] = trans[5]
    
    checkArr=['코스피200', '코스피','코스닥']
    
    if da[0][0] in checkArr:
        checkArr.remove(da[0][0])
        #print(da[0][0])
    if da[0][1] in checkArr:
        checkArr.remove(da[0][1])
        #print(da[0][1])
    if da[0][2] in checkArr:
        checkArr.remove(da[0][2])
        #print(da[0][2])
    if not checkArr:
        print("arr is empty")
        saveData(da,"chart",False)
        print("dataSave!")
        break    