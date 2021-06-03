from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import re

#크롤링에 필요한 함수
def startDate(endTime):
    start = endTime - relativedelta(days=100)
    startDay = str(start.year) + '/'
    if start.month < 10:
        startDay += str(0) + str(start.month) + '/'
    else:
        startDay += str(start.month) + '/'

    if start.day < 10:
        startDay += str(0) + str(start.day) + '/'
    else:
        startDay += str(start.day)
    return startDay
def endDate():
    if parseToday():
        end = datetime.now()
    else :
        end = datetime.now() - relativedelta(days=1)
    endDay = str(end.year) + '/'
    if end.month < 10:
        endDay += str(0) + str(end.month) + '/'
    else:
        endDay += str(end.month) + '/'

    if end.day < 10:
        endDay += str(0) + str(end.day)
    else:
        endDay += str(end.day)
    return endDay
def parseToday():
    if datetime.now().hour>18:
        return True
    elif datetime.now().hour==18 and datetime.now().minute>=4:
        return True
    else:
        return False
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

#코스피 투자자별 매매동향
def KOSPIInvestor():
    if parseToday():
        end=7
    else:
        end=8
    end = 8
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
    header = ['일자', '개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']
    d.columns = header
    d[['개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']] \
        = d[['개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']].apply(pd.to_numeric)
    for col in d.columns:
        if col == '일자': continue
        d[col] *= 100
    d = d[::-1]
    d=d[-60:]
    d = d.reset_index(drop=True)
    return d

#코스닥 투자자별 매매동향
def KOSDAQInvestor():
    if parseToday():
        end=7
    else:
        end=8
    end = 8
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
            if datetime.today().weekday()!=5 and datetime.today().weekday()!=6:
                start=14+11
        for j in range(start, 14 + 11 * 10, 11):
            if i == 1 and j == start:
                d = pd.DataFrame(data[j:j + 11]).T
            else:
                d = pd.concat([d, pd.DataFrame(data[j:j + 11]).T], axis=0)
    header = ['일자', '개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']
    d.columns = header
    d[['개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']]=d[['개인', '외국인', '기관', '금융투자', '보험', '투신(사모)', '은행', '기타금융', '연기금 등', '기타']].apply(pd.to_numeric)
    for col in d.columns:
        if col=='일자': continue
        d[col]*=100
    d=d[::-1]
    d=d[-60:]
    d=d.reset_index(drop=True)
    return d

#investing.com 크롤링
def makeInputData(URL, name, oneColumns):
    # 옵션 생성 - 창 숨기기 추가
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")

    #driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.implicitly_wait(30)
    driver.get(url=URL)

    if parseToday():
        end = datetime.now()
    else:
        end = datetime.now() - relativedelta(days=1)

    try:
        driver.find_element_by_xpath('//*[@id="widgetFieldDateRange"]').click()
    except:
        driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
        driver.find_element_by_xpath('//*[@id="widgetFieldDateRange"]').click()
    print('%s / click' %name)
    try:
        driver.find_element_by_xpath('//*[@id="startDate"]').clear()
    except:
        driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
        driver.find_element_by_xpath('//*[@id="startDate"]').clear()
    print('%s / clear startDate' %name)
    try:
        driver.find_element_by_xpath('//*[@id="startDate"]').send_keys(startDate(end))
    except:
        driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
        driver.find_element_by_xpath('//*[@id="startDate"]').send_keys(startDate(end))
    print('%s / enter start date : %s' %(name,startDate(end)))
    try:
        driver.find_element_by_xpath('//*[@id="endDate"]').clear()
    except:
        driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
        driver.find_element_by_xpath('//*[@id="endDate"]').clear()
    print('%s / clear endDate'%name)
    try:
        driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(endDate())
    except:
        driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
        driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(endDate())
    print('%s / enter end date : %s' %(name,endDate()))
    try:
        driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(Keys.RETURN)
    except:
        driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
        driver.find_element_by_xpath('//*[@id="endDate"]').send_keys(Keys.RETURN)
    print('%s / send data'%name)


    header = []
    if oneColumns:
        header=[name]
        start=2
        end = 3
    else :
        header=['close', 'open','high','low','volume','대비%']
        start=2
        end = 8
    data = []
    for i in range(1, 66):
        line = []
        for j in range(start, end):
            try:
                line.append(
                    driver.find_element_by_xpath('//*[@id="curr_table"]/tbody/tr[' + str(i) + ']/td[' + str(j) + ']').text.replace(',',''))
            except:
                driver.find_element_by_xpath('//*[@id="PromoteSignUpPopUp"]/div[2]/i').click()
                line.append(
                    driver.find_element_by_xpath('//*[@id="curr_table"]/tbody/tr[' + str(i) + ']/td[' + str(j) + ']').text.replace(',',''))
        data.append(line)
    data = pd.DataFrame(data)
    data.columns = header
    if not oneColumns:
        data[['close', 'open','high','low']] = data[['close', 'open','high','low']].apply(pd.to_numeric)
    else:
        data[header]=data[header].apply(pd.to_numeric)
    if not oneColumns:
        cont=[]
        for i in range(len(data.index)-1):
            cont.append(data['close'][i]-data['close'][i+1])
        cont=pd.DataFrame(cont)
        cont.columns=['대비']
        cont=cont[:60]
        data=data[:60]
        data=pd.concat([data, cont], axis=1)
    else:
        data=data[:60]
    data = data[::-1]
    data=data.reset_index(drop=True)
    driver.quit()
    return name, data

def makeModelInput():

    totalColumns=['일자','close','대비','기관','외국인','개인','기타',
              '금융투자','보험','투신(사모)','은행','기타금융','연기금 등',
              'open','high','low','volume','대비%','한국금리',
              '천연가스','미국금리','다우존스','나스닥','구리','WTI']


    name = ['kosdaq', 'kospi', '나스닥', '다우존스', '천연가스', '구리', 'WTI']
    oneColumns=[False, False, True, True, True, True, True]
    urls = ['https://kr.investing.com/indices/kosdaq-historical-data',
            'https://kr.investing.com/indices/kospi-historical-data',
            'https://kr.investing.com/indices/nq-100-futures-historical-data',
            'https://kr.investing.com/indices/us-30-historical-data',
            'https://kr.investing.com/commodities/natural-gas-historical-data',
            'https://kr.investing.com/commodities/copper-historical-data',
            'https://kr.investing.com/commodities/crude-oil-historical-data']
    pool = ThreadPoolExecutor(max_workers=7)
    dataList = list(pool.map(makeInputData, urls, name, oneColumns))
    name.clear()
    data=[]
    addDataName=[]
    addData=[]
    for d in dataList:
        if list(d)[0]=='kospi' or list(d)[0]=='kosdaq':
            name.append(list(d)[0])
            data.append(list(d)[1])
        else :
            addDataName.append(list(d)[0])
            addData.append(list(d)[1])

    dataList.clear()
    for i in range(len(name)):
        if name[i]=='kospi':
            for j in range(len(addDataName)):
                data[i] = pd.concat([data[i], addData[j]], axis=1)
            data[i]=pd.concat([data[i],KOSPIInvestor()],axis=1)
            data[i]['한국금리']=0.5
            data[i]['미국금리']=0.25
            data[i]=data[i][totalColumns]
        elif name[i]=='kosdaq':
            for j in range(len(addDataName)):
                data[i] = pd.concat([data[i], addData[j]], axis=1)
            data[i]=pd.concat([data[i],KOSDAQInvestor()],axis=1)
            data[i]['한국금리']=0.5
            data[i]['미국금리']=0.25
            data[i]=data[i][totalColumns]
    print(name, data)
    return name, data