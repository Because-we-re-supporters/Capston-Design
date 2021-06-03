import pandas as pd
data1 = pd.read_csv('static/result/kosdaq_result.csv')
data2 = pd.read_csv('static/result/kospi_result.csv')
arr=[]
rr=[]
for i in data1['종목명']:
    arr.append(i)

for i in data2['종목명']:
    rr.append(i)
print(arr)
print(rr)