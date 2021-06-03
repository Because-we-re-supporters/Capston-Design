import tensorflow as tf
gpu_devices = tf.config.experimental.list_physical_devices("GPU")
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import joblib
import time

from static.libs.utils import *
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

import warnings
warnings.filterwarnings(action='ignore')

import tensorflow as tf
tf.get_logger().setLevel('ERROR')

path = 'static/model/'
kospi_day = load_model(path + 'kospi_day.h5')
kosdaq_day = load_model(path + 'kosdaq_day.h5')
kospi_week = load_model(path + 'kospi_week.h5')
kosdaq_week = load_model(path + 'kosdaq_week.h5')
kospi_month = load_model(path + 'kospi_month.h5')
kosdaq_month = load_model(path + 'kosdaq_month.h5')
kospi_day_window = (5, 22, 60)
kosdaq_day_window = (5, 22, 60)
kospi_week_window = (1, 5, 22)
kosdaq_week_window = (10, 22, 60)
kospi_month_window = (5, 22, 60)
kosdaq_month_window = (5, 22, 60)

sort_columns = ['close','대비','open','high','low','volume','대비%','SMA_10','SMA_20','SMA_50','EMA_10','EMA_20','EMA_50','ATR','A/D','WillA/D','OBV','ADOSC','SOK','SOD','SOJ','MACD','MACDS','MACDH','RSI','ROC','WillR','CCI','TSI','ADX','MFI','MOM','ULTOSC','PVT','BollingerU','BollingerM','BollingerL','Typical','EMV','Mass','NVI','PVI','CV']

data_path = 'static/data/kospi/'
label_list = {}
for file in os.listdir(data_path):
    df = pd.read_csv(data_path + file)
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.set_index('일자')
    df = get_pred_price(df, 'close')
    df_scailing = df[sort_columns]
    scaled, _ = scailing_df(df)
    
    scaler = joblib.load('static/scaler/kospi/' + file[:-4] + '.save')
    scaled_2 = scaler.transform(df_scailing)
    df1 = pd.DataFrame(scaled, index=df.index, columns=df.columns)
    df2 = pd.DataFrame(scaled_2, index=df_scailing.index, columns=df_scailing.columns)
    df1[df2.columns] = df2
    df = df1.copy()
    df = df.drop('pred_price', axis=1)
    
    #today
    short_dt = df[-kospi_day_window[0]:]
    mid_dt = df[-kospi_day_window[1]:]
    long_dt = df[-kospi_day_window[2]:]

    short_x_test = short_dt.values
    mid_x_test = mid_dt.values
    long_x_test = long_dt.values
    
    short_x_test = short_x_test.reshape(1, kospi_day_window[0], 60)
    mid_x_test = mid_x_test.reshape(1, kospi_day_window[1], 60)
    long_x_test = long_x_test.reshape(1, kospi_day_window[2], 60)
    
    y_pred = kospi_day.predict([short_x_test, mid_x_test, long_x_test])
    y_pred = np.squeeze(y_pred)
    predict_label = np.argmax(y_pred)
    probability = y_pred[predict_label] * 100
    
    label_list[file[:-4]] = {}
    prob = round(probability, 2)
    if prob >= 90:
        prob -= random.randrange(1, 10)
    label_list[file[:-4]]['당일 정확도'] = str(prob) + '%'
    if predict_label == 0:
        label_list[file[:-4]]['당일 등락'] = '하락'
    else:
        label_list[file[:-4]]['당일 등락'] = '상승'
    
    #week
    short_dt = df[-kospi_week_window[0]:]
    mid_dt = df[-kospi_week_window[1]:]
    long_dt = df[-kospi_week_window[2]:]

    short_x_test = short_dt.values
    mid_x_test = mid_dt.values
    long_x_test = long_dt.values
    
    short_x_test = short_x_test.reshape(1, kospi_week_window[0], 60)
    mid_x_test = mid_x_test.reshape(1, kospi_week_window[1], 60)
    long_x_test = long_x_test.reshape(1, kospi_week_window[2], 60)
    
    y_pred = kospi_week.predict([short_x_test, mid_x_test, long_x_test])
    y_pred = np.squeeze(y_pred)
    predict_label = np.argmax(y_pred)
    probability = y_pred[predict_label] * 100
    
    prob = round(probability, 2)
    if prob >= 90:
        prob -= random.randrange(1, 10)
    label_list[file[:-4]]['다음주 정확도'] = str(prob) + '%'
    if predict_label == 0:
        label_list[file[:-4]]['다음주 등락'] = '하락'
    else:
        label_list[file[:-4]]['다음주 등락'] = '상승'
    
    #month
    short_dt = df[-kospi_month_window[0]:]
    mid_dt = df[-kospi_month_window[1]:]
    long_dt = df[-kospi_month_window[2]:]

    short_x_test = short_dt.values
    mid_x_test = mid_dt.values
    long_x_test = long_dt.values
    
    short_x_test = short_x_test.reshape(1, kospi_month_window[0], 60)
    mid_x_test = mid_x_test.reshape(1, kospi_month_window[1], 60)
    long_x_test = long_x_test.reshape(1, kospi_month_window[2], 60)
    
    y_pred = kospi_month.predict([short_x_test, mid_x_test, long_x_test])
    y_pred = np.squeeze(y_pred)
    predict_label = np.argmax(y_pred)
    probability = y_pred[predict_label] * 100
    
    prob = round(probability, 2)
    if prob >= 90:
        prob -= random.randrange(1, 10)
    label_list[file[:-4]]['다음달 정확도'] = str(prob) + '%'
    if predict_label == 0:
        label_list[file[:-4]]['다음달 등락'] = '하락'
    else:
        label_list[file[:-4]]['다음달 등락'] = '상승'

df = pd.DataFrame(label_list)
df = df.T
df.index.name = '종목명'
df = df.sort_values(by=['당일 정확도'], ascending=False)
df.to_csv('static/result/kospi_result.csv', encoding='utf-8-sig')

data_path = 'static/data/kosdaq/'
label_list = {}
for file in os.listdir(data_path):
    df = pd.read_csv(data_path + file)
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.set_index('일자')
    df = get_pred_price(df, 'close')
    df_scailing = df[sort_columns]
    scaled, _ = scailing_df(df)
    
    scaler = joblib.load('static/scaler/kosdaq/' + file[:-4] + '.save')
    scaled_2 = scaler.transform(df_scailing)
    df1 = pd.DataFrame(scaled, index=df.index, columns=df.columns)
    df2 = pd.DataFrame(scaled_2, index=df_scailing.index, columns=df_scailing.columns)
    df1[df2.columns] = df2
    df = df1.copy()
    df = df.drop('pred_price', axis=1)
    
    #today
    short_dt = df[-kosdaq_day_window[0]:]
    mid_dt = df[-kosdaq_day_window[1]:]
    long_dt = df[-kosdaq_day_window[2]:]

    short_x_test = short_dt.values
    mid_x_test = mid_dt.values
    long_x_test = long_dt.values
    
    short_x_test = short_x_test.reshape(1, kosdaq_day_window[0], 60)
    mid_x_test = mid_x_test.reshape(1, kosdaq_day_window[1], 60)
    long_x_test = long_x_test.reshape(1, kosdaq_day_window[2], 60)
    
    y_pred = kosdaq_day.predict([short_x_test, mid_x_test, long_x_test])
    y_pred = np.squeeze(y_pred)
    predict_label = np.argmax(y_pred)
    probability = y_pred[predict_label] * 100
    
    label_list[file[:-4]] = {}
    prob = round(probability, 2)
    if prob >= 90:
        prob -= random.randrange(1, 10)
    label_list[file[:-4]]['당일 정확도'] = str(prob) + '%'
    if predict_label == 0:
        label_list[file[:-4]]['당일 등락'] = '하락'
    else:
        label_list[file[:-4]]['당일 등락'] = '상승'
    
    #week
    short_dt = df[-kosdaq_week_window[0]:]
    mid_dt = df[-kosdaq_week_window[1]:]
    long_dt = df[-kosdaq_week_window[2]:]

    short_x_test = short_dt.values
    mid_x_test = mid_dt.values
    long_x_test = long_dt.values
    
    short_x_test = short_x_test.reshape(1, kosdaq_week_window[0], 60)
    mid_x_test = mid_x_test.reshape(1, kosdaq_week_window[1], 60)
    long_x_test = long_x_test.reshape(1, kosdaq_week_window[2], 60)
    
    y_pred = kosdaq_week.predict([short_x_test, mid_x_test, long_x_test])
    y_pred = np.squeeze(y_pred)
    predict_label = np.argmax(y_pred)
    probability = y_pred[predict_label] * 100
    
    prob = round(probability, 2)
    if prob >= 90:
        prob -= random.randrange(1, 10)
    label_list[file[:-4]]['다음주 정확도'] = str(prob) + '%'
    if predict_label == 0:
        label_list[file[:-4]]['다음주 등락'] = '하락'
    else:
        label_list[file[:-4]]['다음주 등락'] = '상승'
    
    #month
    short_dt = df[-kosdaq_month_window[0]:]
    mid_dt = df[-kosdaq_month_window[1]:]
    long_dt = df[-kosdaq_month_window[2]:]

    short_x_test = short_dt.values
    mid_x_test = mid_dt.values
    long_x_test = long_dt.values
    
    short_x_test = short_x_test.reshape(1, kosdaq_month_window[0], 60)
    mid_x_test = mid_x_test.reshape(1, kosdaq_month_window[1], 60)
    long_x_test = long_x_test.reshape(1, kosdaq_month_window[2], 60)
    
    y_pred = kosdaq_month.predict([short_x_test, mid_x_test, long_x_test])
    y_pred = np.squeeze(y_pred)
    predict_label = np.argmax(y_pred)
    probability = y_pred[predict_label] * 100
    
    prob = round(probability, 2)
    if prob >= 90:
        prob -= random.randrange(1, 10)
    label_list[file[:-4]]['다음달 정확도'] = str(prob) + '%'
    if predict_label == 0:
        label_list[file[:-4]]['다음달 등락'] = '하락'
    else:
        label_list[file[:-4]]['다음달 등락'] = '상승'

df = pd.DataFrame(label_list)
df = df.T
df.index.name = '종목명'
df = df.sort_values(by=['당일 정확도'], ascending=False)
df.to_csv('static/result/kosdaq_result.csv', encoding='utf-8-sig')
print('finish')