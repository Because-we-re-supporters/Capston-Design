import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

kospi_path = 'static/result/kospi_mock.csv'
kosdaq_path = 'static/result/kosdaq_mock.csv'
kospi_df = pd.read_csv(kospi_path)
kosdaq_df = pd.read_csv(kosdaq_path)
kospi_df = kospi_df.set_index('day')
kosdaq_df = kosdaq_df.set_index('day')

kospi_result_df = pd.read_csv('static/result/kospi_result.csv')
kosdaq_result_df = pd.read_csv('static/result/kosdaq_result.csv')
kospi_result_df = kospi_result_df.set_index('종목명')
kosdaq_result_df = kosdaq_result_df.set_index('종목명')

mock = pd.read_csv('static/result/mock.csv')
mock = mock.set_index('index')

kospi_top1 = mock.loc['top1', 'KOSPI']
kosdaq_top1 = mock.loc['top1', 'KOSDAQ']
kospi_data_path = 'static/data/kospi/'
kosdaq_data_path = 'static/data/kosdaq/'

kospi_top_df = pd.read_csv(kospi_data_path + kospi_top1 + '.csv')
kosdaq_top_df = pd.read_csv(kosdaq_data_path + kosdaq_top1 + '.csv')
kospi_top_df = kospi_top_df.set_index('일자')
kosdaq_top_df = kosdaq_top_df.set_index('일자')
kospi_top_df = kospi_top_df[['close']][-2:]
kosdaq_top_df = kosdaq_top_df[['close']][-2:]

kospi_profit = kospi_top_df['close'][-1] / kospi_top_df['close'][-2]
kosdaq_profit = kosdaq_top_df['close'][-1] / kosdaq_top_df['close'][-2]
kospi_profit = round(kospi_profit * 100 - 100, 2)
kosdaq_profit = round(kosdaq_profit * 100 - 100, 2)

kospi_df = kospi_df[1:].copy()
kospi_df.index = [x for x in range(1, 30)]
kosdaq_df = kosdaq_df[1:].copy()
kosdaq_df.index = [x for x in range(1, 30)]

kospi_df.loc[30] = [kospi_profit, kospi_profit > 0, round(kospi_df.loc[29, 'KOSPI 누적 수익률'] + kospi_profit, 2)]
kosdaq_df.loc[30] = [kosdaq_profit, kosdaq_profit > 0, round(kosdaq_df.loc[29, 'KOSDAQ 누적 수익률'] + kosdaq_profit, 2)]

kospi_table = pd.read_csv('static/result/kospi_table.csv')
kosdaq_table = pd.read_csv('static/result/kosdaq_table.csv')
kospi_table = kospi_table.set_index('종목')
kosdaq_table = kosdaq_table.set_index('종목')

kospi_table.loc['KOSPI', '투자 수익'] = str(round(int(1000000 * kospi_df.loc[30, 'KOSPI 누적 수익률']), -4))[:3] + ' 만원'
kospi_table.loc['KOSPI', '적중률'] = str(round(kospi_df['KOSPI 적중'].value_counts()[True] / 30, 4) * 100) + '%'
kospi_table.loc['KOSPI', '최대 수익률'] = str(kospi_df['KOSPI 수익률'].max()) + '%'
kospi_table.loc['KOSPI', '누적 수익률'] = str(round(kospi_df.loc[30, 'KOSPI 누적 수익률'], 2)) + '%'
kosdaq_table.loc['KOSDAQ', '투자 수익'] = str(round(int(1000000 * kosdaq_df.loc[30, 'KOSDAQ 누적 수익률']), -4))[:3] + ' 만원'
kosdaq_table.loc['KOSDAQ', '적중률'] = str(round(kosdaq_df['KOSDAQ 적중'].value_counts()[True] / 30, 4) * 100) + '%'
kosdaq_table.loc['KOSDAQ', '최대 수익률'] = str(kosdaq_df['KOSDAQ 수익률'].max()) + '%'
kosdaq_table.loc['KOSDAQ', '누적 수익률'] = str(round(kosdaq_df.loc[30, 'KOSDAQ 누적 수익률'], 2)) + '%'

kp_top1 = kospi_result_df.index[0]
kd_top1 = kosdaq_result_df.index[0]
mock.loc['top1', 'KOSPI'] = kp_top1
mock.loc['top1', 'KOSDAQ'] = kd_top1


kospi_df.to_csv('static/result/kospi_mock.csv', encoding='utf-8-sig')
kosdaq_df.to_csv('static/result/kospdaq_mock.csv', encoding='utf-8-sig')
kospi_table.to_csv('static/result/kospi_table.csv', encoding='utf-8-sig')
kosdaq_table.to_csv('static/result/kosdaq_table.csv', encoding='utf-8-sig')
mock.to_csv('static/result/mock.csv', encoding='utf-8-sig')
print('finish')