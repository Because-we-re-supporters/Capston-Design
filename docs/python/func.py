import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import os
from datetime import datetime
import urllib.request as req
import re

def saveData(data, name, flag):
    src="C:/Users/tn12q/Documents/Capston-Design/docs/data/"
    makeDir(src)
    makeDir(src+'totalData/')
    data.to_csv(src+'totalData/'+datetime.today().strftime("%Y%m%d_%H%M%S")+name+'.txt',encoding='utf-8', sep=';', index=flag)
    data.to_csv(src+name+'.txt',encoding='utf-8', sep=';', index=flag)
    print("Data saving is complete!")

def removeTag(x):
    x=str(x)
    x=re.sub('<.+?>', '', x, 0).strip()
    x=x.replace('[','')
    x=x.replace(']','')
    return x

def makeDir(path):
    print(path)
    if not os.path.isdir(path):                                                           
        os.mkdir(path)