from keras.models import load_model
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import tensorflow.keras.backend as kb
import warnings
from inverstingCrawling import makeModelInput

warnings.filterwarnings(action='ignore')
tf.get_logger().setLevel('ERROR')
def get_df(df):
    df = df['일자', 'close', '기관', '외국인', '개인', '연기금 등', '한국금리', '다우존스', 'WTI', '구리', '천연가스', '나스닥', '미국금리']
    df['일자'] = pd.to_datetime(df['일자'])
    df.columns = ['Date', 'Stock', 'Institution', 'Foreginer', 'Individual', 'Pension',
                  'Interest rate', 'Dowjones', 'WTI', 'Copper', 'Natural gas', 'Nasdaq', 'Interest rate_A']
    df = df.set_index('Date')
    df = df.sort_index()
    df = df.dropna()

    return df
def normalize_df(df):
    scalers = {}
    df_scaled = pd.DataFrame(columns = df.columns, index = df.index)
    for col in df.columns:
        scaler = MinMaxScaler(feature_range = (0,1))
        scaled = scaler.fit_transform(df[[col]])
        df_scaled[col] = scaled
        scalers[col] = scaler
    return df_scaled, scalers
def inverse_data(data, max_value, min_value):
    data = (data * (max_value - min_value)) + min_value
    return data
def RMSE(d_max, d_min):
    def loss(y_test, y_pred):
        y_test = inverse_data(y_test, d_max, d_min)
        y_pred = inverse_data(y_pred, d_max, d_min)
        rmse_loss = kb.sqrt(kb.mean(kb.square(y_pred - y_test)))
        return rmse_loss
    loss.__name__ = 'rmse'
    return loss
def MPE(d_max, d_min):
    def loss(y_test, y_pred):
        y_test = inverse_data(y_test, d_max, d_min)
        y_pred = inverse_data(y_pred, d_max, d_min)
        mpe_loss = kb.mean((y_pred - y_test) / y_test) * 100
        return mpe_loss

    loss.__name__ = 'mpe'
    return loss

def loadKOSDAQ(df):
    labels = ['Stock']
    features =['Stock', 'Interest rate', 'Natural gas', 'Individual']
    df_norm, scalers = normalize_df(df)
    df_scaled=df_norm[-60:]
    x, y = df_scaled[features], df_scaled['Stock']
    x=x.to_numpy().reshape(1,-1,4)
    model = load_model('static/model/KOSDAQ.h5', custom_objects={'RMSE': RMSE, 'MPE': MPE})
    result=model.predict(x)[0][0]
    value = inverse_data(result, df['Stock'].max(), df['Stock'].min())
    #print("KOSDAQ: %.2f" %value)
    return value
def loadKOSPI(df):
    labels = ['Stock']
    features = ['Stock', 'Interest rate']

    df = get_df('KOSPI')
    df_norm, scalers = normalize_df(df)
    df_scaled=df_norm[-30:]
    x, y = df_scaled[features], df_scaled['Stock']
    x=x.to_numpy().reshape(1,-1,2)
    model = load_model('static/model/KOSPI.h5', custom_objects={'RMSE':RMSE,'MPE':MPE})
    result=model.predict(x)[0][0]
    value=inverse_data(result,df['Stock'].max(),df['Stock'].min())
    #print("KOSPI: %.2f" %value)
    return value

name, dfList = makeModelInput()
print(type(dfList[0]))
print(type(dfList[1]))
for i in range(len(name)):
    if name[i]=='kospi':
        print(loadKOSPI(get_df(dfList[i])))
    elif name[i]=='kosdaq':
        print(loadKOSDAQ(get_df(dfList[i])))


