import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

import talib as tas
from ta.momentum import tsi

warnings.filterwarnings(action='ignore')

def get_extraction_df(file, open_file, add_file):
    file_path = 'data/' + file + '.csv'
    df = pd.read_csv(file_path, thousands = ',')
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.set_index('일자')
    df = df.sort_index()
    df = df.drop(['국가','외인-기타','외국인합','기타법인','합계'], axis=1)
    
    file_path = 'data/' + add_file + '.csv'
    add_df = pd.read_csv(file_path, thousands=',', encoding='CP949')
    add_df = add_df.dropna()
    add_df['일자'] = pd.to_datetime(add_df['일자'])
    add_df = add_df.set_index('일자')
    add_df = add_df.sort_index()
    
    file_path = 'data/' + open_file + '_open.csv'
    open_df = pd.read_csv(file_path, thousands=',')
    
    for i in range(len(open_df)):
        date = open_df.iloc[i]['날짜']
        y = date[:4]
        m = date[6:8]
        d = date[10:12]
        date = '-'.join([y,m,d])
        open_df.loc[i, '날짜'] = date
        
        volume = open_df.iloc[i]['거래량']
        if 'M' in volume:
            vol = float(volume[:-1]) * 1000000
        elif 'B' in volume:
            vol = float(volume[:-1]) * 1000000000
        elif 'K' in volume:
            vol = float(volume[:-1]) * 1000
        open_df.loc[i, '거래량'] = int(vol)
        
        change = open_df.iloc[i]['변동 %']
        open_df.loc[i, '변동 %'] = float(change[:-1])
    open_df.columns = ['일자', '지수', '오픈', '고가', '저가', '거래량', '대비%']
    open_df = open_df.drop(['지수'], axis=1)
    open_df['일자'] = pd.to_datetime(open_df['일자'])
    open_df = open_df.set_index('일자')
    open_df = open_df.sort_index()
    open_df['대비%'] = open_df['대비%'].astype('float64')
    open_df['거래량'] = open_df['거래량'].astype('int64')
    
    merge = pd.merge(df, open_df, on='일자')
    merge = pd.merge(merge, add_df, on='일자')
    
    merge.columns = ['close', '대비', '기관', '외국인', '개인', '기타', '금융투자', 
                     '보험', '투신', '사모', '은행', '기타금융', '연기금 등',
                     'open', 'high', 'low', 'volume',  '대비%', '한국금리',
                     '천연가스', '미국금리', '다우존스', '나스닥', '구리', 'WTI']
    
    return merge

def SMA(df, window):
    columns = 'SMA_' + str(window)
    df[columns] = df['close'].rolling(window).mean()
    return df

def EMA(df, window):
    columns = 'EMA_' + str(window)
    df[columns] = df['close'].ewm(window).mean()
    return df

def Feature_Extraction_Moving_Average(df):
    df = SMA(df, 10)
    df = SMA(df, 20)
    df = SMA(df, 50)
    df = EMA(df, 10)
    df = EMA(df, 20)
    df = EMA(df, 50)
    
    df = df.fillna(0)
    return df

def Feature_Extraction_Volatility(df):
    df['ATR'] = tas.ATR(df['high'].values, df['low'].values, df['close'].values)
    df = df.fillna(0)
    return df

def Williams_AD(df):
    df['WillA/D'] = 0.
    
    for i in range(len(df)):
        row = df.iloc[i]
        idx = i
        if idx > 0:
            prev_value = df.iloc[idx-1]['WillA/D']
            prev_close = df.iloc[idx-1]['close']
            
            if row['close'] > prev_close:
                ad = row['close'] - min(prev_close, row['low'])
            elif row['close'] < prev_close:
                ad = row['close'] - max(prev_close, row['high'])
            else:
                ad = 0.
            df.loc[df.index[i], 'WillA/D'] = (ad + prev_value)
    return df

def Feature_Extraction_Volume(df):
    df['A/D'] = tas.AD(df['high'], df['low'], df['close'], df['volume'])
    df = Williams_AD(df)
    df['OBV'] = tas.OBV(df['close'], df['volume'])
    df['ADOSC'] = tas.ADOSC(df['high'], df['low'], df['close'], df['volume'])
    df = df.fillna(0)
    return df

def SOK(df, n=5):
    df['SOK'] = ((df['close'] - df['low'].rolling(n, min_periods=0).min()) / (df['high'].rolling(n, min_periods=0).max() - df['low'].rolling(n, min_periods=0).min())) * 100
    return df

def SOD(df, m=3):
    df['SOD'] = df['SOK'].rolling(m, min_periods=0).mean()
    return df

def SOJ(df, t=3):
    df['SOJ'] = df['SOD'].rolling(t, min_periods=0).mean()
    return df

def MACD(df, short_t=12, long_t=26):
    MA12 = df['close'].ewm(span=short_t, min_periods=0).mean()
    MA26 = df['close'].ewm(span=long_t, min_periods=0).mean()
    df['MACD'] = MA12 - MA26
    return df

def MACD_Signal(df, t=9):
    df['MACDS'] = df['MACD'].ewm(span=t, min_periods=0).mean()
    return df

def MACD_Hist(df):
    df['MACDH'] = df['MACD'] - df['MACDS']
    return df

def Feature_Extraction_Momentum(df):
    df = SOK(df)
    df = SOD(df)
    df = SOJ(df)
    df = MACD(df)
    df = MACD_Signal(df)
    df = MACD_Hist(df)
    df['RSI'] = tas.RSI(df['close'].values)
    df['ROC'] = tas.ROC(df['close'].values)
    df['WillR'] = tas.WILLR(df['high'].values, df['low'].values, df['close'].values)
    df['CCI'] = tas.CCI(df['high'].values, df['low'].values, df['close'].values)
    df['TSI'] = tsi(df['close'], window_slow=25, window_fast=13)
    df['ADX'] = tas.ADX(df['high'].values, df['low'].values, df['close'].values)
    df['MFI'] = tas.MFI(df['high'], df['low'], df['close'], df['volume'])
    df['MOM'] = tas.MOM(df['close'])
    df['TRIX'] = tas.TRIX(df['close'])
    df['ULTOSC'] = tas.ULTOSC(df['high'], df['low'], df['close'])
    
    df = df.fillna(0)
    return df

def PVT(df):
    for i in range(len(df)):
        idx = i
        row = df.iloc[i]
        if idx > 0:
            last_val = df.iloc[idx-1]['PVT']
            last_close = df.iloc[idx-1]['close']
            today_close = row['close']
            today_vol = row['volume']
            current_val = last_val + (today_vol * (today_close - last_close) / last_close)
        else:
            current_val = row['volume']
        df.loc[df.index[i], 'PVT'] = current_val
    return df

def Bollinger_Bands(df):
    upper, middle, lower = tas.BBANDS(df['close'])
    df['BollingerU'] = upper
    df['BollingerM'] = middle
    df['BollingerL'] = lower
    return df

def Typical(df):
    df['Typical'] = (df['high'] + df['low'] + df['close']) / 3
    return df

def EMV(df):
    for i in range(len(df)):
        idx = i
        row = df.iloc[i]
        
        if idx > 0:
            midpoint = (row['high'] + row['low']) / 2 - (df.iloc[idx-1]['high'] + df.iloc[idx-1]['low']) / 2
        else:
            midpoint = 0
        diff = row['high'] - row['low']
        
        if diff == 0:
            diff = 0.000000001
        
        vol = row['volume']
        if vol == 0:
            vol = 1
        box_ratio = (vol / 100000000) / (diff)
        emv = midpoint / box_ratio
        
        df.loc[df.index[i], 'EMV'] = emv
    return df

def Mass(df, t = 25, ema_t = 9):
    high_low = df['high'] - df['low'] + 0.000001
    ema = high_low.ewm(ema_t, min_periods=0).mean()
    ema_ema = ema.ewm(ema_t, min_periods=0).mean()
    div = ema / ema_ema
    
    for i in range(len(df)):
        idx = i
        if idx >= t:
            val = div[idx-t:idx].sum()
        else:
            val = 0
        df.loc[df.index[i], 'Mass'] = val
    return df

def NVI(df):
    df['NVI'] = 0.
    
    for i in range(len(df)):
        idx = i
        row = df.iloc[i]
        
        if idx > 0:
            prev_nvi = df.iloc[idx-1]['NVI']
            prev_close = df.iloc[idx-1]['close']
            
            if row['volume'] < df.iloc[idx-1]['volume']:
                nvi = prev_nvi + (row['close'] - prev_close / prev_close * prev_nvi)
            else:
                nvi = prev_nvi
        else:
            nvi = 1000
        df.loc[df.index[i], 'NVI'] = nvi
    return df

def PVI(df):
    df['PVI'] = 0.
    
    for i in range(len(df)):
        idx = i
        row = df.iloc[i]
        
        if idx > 0:
            prev_pvi = df.iloc[idx-1]['PVI']
            prev_close = df.iloc[idx-1]['close']
            
            if row['volume'] > df.iloc[idx-1]['volume']:
                pvi = prev_pvi + (row['close'] - prev_close / prev_close * prev_pvi)
            else:
                pvi = prev_pvi
        else:
            pvi = 1000
        df.loc[df.index[i], 'PVI'] = pvi
    return df

def CV(df, ema_t=10, change_t=10):
    df['CV_HL'] = df['high'] - df['low']
    df['CV_EMA'] = df['CV_HL'].ewm(ema_t, min_periods=0).mean()
    df['CV'] = 0.
    
    for i in range(len(df)):
        idx = i
        row = df.iloc[i]
        if idx > change_t:
            prev_value = df.iloc[idx-change_t]['CV_EMA']
            if prev_value == 0:
                prev_value = 0.0001
            df.loc[df.index[i], 'CV'] = ((row['CV_EMA'] - prev_value) / prev_value)
    df = df.drop(['CV_HL', 'CV_EMA'], axis=1)
    return df

def Feature_Extraction_Other(df):
    df = PVT(df)
    df = Bollinger_Bands(df)
    df = Typical(df)
    df = EMV(df)
    df = Mass(df)
    df = NVI(df)
    df = PVI(df)
    df = CV(df)
    
    df = df.fillna(0)
    return df

def Feature_Extraction(df, verbose=True):
    if verbose: print('Loading...')
    df = Feature_Extraction_Moving_Average(df)
    if verbose: print('Finish Moving Average')
    if verbose: print('Loading...')
    df = Feature_Extraction_Volatility(df)
    if verbose: print('Finish Volatility')
    if verbose: print('Loading...')
    df = Feature_Extraction_Volume(df)
    if verbose: print('Finish Volume')
    if verbose: print('Loading...')
    df = Feature_Extraction_Momentum(df)
    if verbose: print('Finish Momentum')
    if verbose: print('Loading...')
    df = Feature_Extraction_Other(df)
    if verbose: 
        print('Finish All')
        print('Number of Features:', len(df.columns))
        print('Number of Datas:', len(df.index))
    return df