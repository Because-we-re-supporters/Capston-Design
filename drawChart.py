import pandas as pd
import plotly as py
from plotly.graph_objs import Scatter, Layout

def updateChart():
    df = pd.read_csv('static/result/kospi_mock.csv', thousands=',', encoding='utf-8')
    print(df.columns)
    py.offline.plot({
        'data':[Scatter(x=df['day'],y=df['KOSPI 누적 수익률'], name='KOSPI 누적 수익률')]
    },filename='templates/MockChart.html',auto_open = False)

def updateChart2():
    df = pd.read_csv('static/result/kosdaq_mock.csv', thousands=',', encoding='utf-8')
    print(df.columns)
    py.offline.plot({
        'data':[Scatter(x=df['day'],y=df['KOSDAQ 누적 수익률'], name='KOSDAQ 누적 수익률')]
    },filename='templates/MockChart2.html',auto_open = False)

def resultChart(name, isKOSPI):
    def resultTable(name, isKOSPI):
        if isKOSPI:
            df = pd.read_csv('static/result/kospi_result.csv', encoding='utf-8')
        else:
            df = pd.read_csv('static/result/kosdaq_result.csv', encoding='utf-8')
        result = df[df['종목명']==name]
        result.to_csv('static/result/resultChart.csv', encoding='utf-8-sig', index=False)
        return
    resultTable(name,isKOSPI)
    if isKOSPI:
        src='static/data/kospi/'
    else:
        src='static/data/kosdaq/'
    print(src+name+'.csv')
    df = pd.read_csv(src+name+'.csv', encoding='utf-8')
    py.offline.plot({
        'data':[Scatter(x=df['일자'],y=df['close'], name='actual')]
    },filename='templates/searchResultChart.html',auto_open = False)

