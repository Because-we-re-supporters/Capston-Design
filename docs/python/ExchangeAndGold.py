import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import os
from datetime import datetime
import urllib.request as req
import re

from func import *

url = "http://finance.naver.com/marketindex/"
res = req.urlopen(url)
soup = BeautifulSoup(res, "html.parser", from_encoding='euc-kr')

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