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