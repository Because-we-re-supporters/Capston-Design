import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import precision_recall_fscore_support
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model

def get_df(data_path, file_path):
    path = 'data/' + data_path + '/' + file_path + '.csv'
    df = pd.read_csv(path)
    df['일자'] = pd.to_datetime(df['일자'])
    df = df.set_index('일자')
    return df

def get_pred_price(df, col, shift=1):
    df['pred_price'] = np.where(df[col].shift(-shift) > df[col], 1, 0)
    return df

def get_next_close(df, col, shift=1):
    df['next_close'] = df[col].shift(-shift)
    return df

def scailing_df(df):
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(scaled, columns=df.columns, index=df.index)
    return df_scaled, scaler

def split_df(df):
    train_len = int((len(df) - 1) * 0.8)
    train = df[:train_len]
    test = df[train_len:]
    return train, test

def windowing_dataset(feature, label, window_size):
    feature_list = []
    label_list = []
    
    for i in range(len(feature) - window_size):
        feature_list.append(np.array(feature.iloc[i:i+window_size]))
        label_list.append(np.array(label.iloc[i+window_size-1]))
    return np.array(feature_list), np.array(label_list)

def make_dataset(df, train, test, window, col='pred_price'):
    train_test_set = []
    data_list = [train, test]
    feature_list = df.columns.difference([col])
    target = col
    
    for data in data_list:
        feature, label = data[feature_list], data[target]
        train_test_set.append(windowing_dataset(feature, label, window))
    return train_test_set

def make_dataset_multi_input(df, train, test, window, col='pred_price'):
    short_dataset = make_dataset(df, train, test, window[0], col)
    mid_dataset = make_dataset(df, train, test, window[1], col)
    long_dataset = make_dataset(df, train, test,window[2], col)
    
    return short_dataset, mid_dataset, long_dataset

def categorical_data(y_train, y_test):
    y_train = to_categorical(y_train, 2, dtype='int32')
    y_test = to_categorical(y_test, 2, dtype='int32')
    return y_train, y_test

def reshape_multi_input(short_x_train, mid_x_train, short_x_test, mid_x_test, window):
    short_x_train_t = short_x_train[:-(window[2] - window[0])]
    mid_x_train_t = mid_x_train[:-(window[2] - window[1])]
    short_x_test_t = short_x_test[:-(window[2] - window[0])]
    mid_x_test_t = mid_x_test[:-(window[2] - window[1])]
    
    return short_x_train_t, mid_x_train_t, short_x_test_t, mid_x_test_t

def predict_model(model, x_test, y_test):
    pred = model.predict(x_test)
    y_pred = np.argmax(pred, axis=1)
    y_true = np.argmax(y_test, axis=1)
    
    prec, recall, fscore, _ = precision_recall_fscore_support(y_true, y_pred)
    
    return prec, recall, fscore

def inverse_data(data, max_value, min_value):
    data = (data * (max_value - min_value)) + min_value
    return data

def MAE(d_max, d_min):
    def loss(y_test, y_pred):
        y_test = inverse_data(y_test, d_max, d_min)
        y_pred = inverse_data(y_pred, d_max, d_min)
        mae_loss = kb.mean(kb.abs(y_pred - y_test))
        return mae_loss
    loss.__name__ = 'mae'
    return loss

def RMSE(d_max, d_min):
    def loss(y_test, y_pred):
        y_test = inverse_data(y_test, d_max, d_min)
        y_pred = inverse_data(y_pred, d_max, d_min)
        rmse_loss = kb.sqrt(kb.mean(kb.square(y_pred - y_test)))
        return rmse_loss
    loss.__name__ = 'rmse'
    return loss

def MAPE(d_max, d_min):
    def loss(y_test, y_pred):
        y_test = inverse_data(y_test, d_max, d_min)
        y_pred = inverse_data(y_pred, d_max, d_min)
        mape_loss = kb.mean(kb.abs((y_pred - y_test) / y_test)) * 100
        return mape_loss
    loss.__name__ = 'mape'
    return loss

def MPE(d_max, d_min):
    def loss(y_test, y_pred):
        y_test = inverse_data(y_test, d_max, d_min)
        y_pred = inverse_data(y_pred, d_max, d_min)
        mpe_loss = kb.mean((y_pred - y_test) / y_test) * 100
        return mpe_loss
    loss.__name__ = 'mpe'
    return loss

def load_best_model(path, scaler):
    model = load_model(path, compile=False)
    max_v, min_v = scaler.data_max_[-1], scaler.data_min_[-1]
    model.compile(optimizer='adam', loss=RMSE(max_v, min_v), metrics=[
        MAE(max_v, min_v), MAPE(max_v, min_v), MPE(max_v, min_v)
    ])
    return model

def predict_reg(model, x_test, y_test, scaler):
    y_pred = model.predict(x_test)
    y_pred = np.squeeze(y_pred)
    
    max_v, min_v = scaler.data_max_[-1], scaler.data_min_[-1]
    
    y_test = inverse_data(y_test, max_v, min_v)
    y_pred = inverse_data(y_pred, max_v, min_v)
    
    mae = np.mean(np.abs(y_pred - y_test))
    rmse = np.sqrt(np.mean(np.square(y_pred - y_test)))
    mape = np.mean(np.abs((y_pred - y_test) / y_test)) * 100
    mpe = np.mean((y_pred - y_test) / y_test) * 100
    
    return mae, rmse, mape, mpe