import tensorflow as tf
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Conv1D, MaxPooling1D, LSTM, GRU, Dropout, SimpleRNN, concatenate, Input, Flatten
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import ModelCheckpoint

def create_dnn(dropout_rate, input_size):
    model = Sequential()
    model.add(Flatten(input_shape=input_size))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(2, activation='softmax'))
    
    return model

def create_cnn(dropout_rate, input_size):
    model = Sequential()
    model.add(Input(shape=input_size))
    model.add(Conv1D(32, 2, activation='relu'))
    model.add(Conv1D(64, 2, activation='relu'))
    model.add(MaxPooling1D(2))
    model.add(Flatten())
    model.add(Dropout(dropout_rate))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(2, activation='softmax'))
    
    return model

def create_rnn(dropout_rate, input_size):
    model = Sequential()
    model.add(SimpleRNN(32, return_sequences=True, input_shape=input_size))
    model.add(SimpleRNN(64, return_sequences=False,))
    model.add(Dropout(dropout_rate))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(2, activation='softmax'))
    
    return model

def create_lstm(dropout_rate, input_size):
    model = Sequential()
    model.add(LSTM(32, return_sequences=True, input_shape=input_size))
    model.add(LSTM(64, return_sequences=False,))
    model.add(Dropout(dropout_rate))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(2, activation='softmax'))
    
    return model

def create_gru(dropout_rate, input_size):
    model = Sequential()
    model.add(GRU(32, return_sequences=True, input_shape=input_size))
    model.add(GRU(64, return_sequences=False,))
    model.add(Dropout(dropout_rate))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(2, activation='softmax'))
    
    return model

def create_cnn_rnn(dropout_rate, input_size):
    model = Sequential()
    model.add(Input(shape=input_size))
    model.add(Conv1D(32, 1, activation='relu', padding='same'))
    model.add(Conv1D(64, 1, activation='relu', padding='same'))
    model.add(MaxPooling1D(1))
    model.add(SimpleRNN(64))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    
    return model

def create_cnn_lstm(dropout_rate, input_size):
    model = Sequential()
    model.add(Input(shape=input_size))
    model.add(Conv1D(32, 1, activation='relu', padding='same'))
    model.add(Conv1D(64, 1, activation='relu', padding='same'))
    model.add(MaxPooling1D(1))
    model.add(LSTM(64))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    
    return model

def create_cnn_gru(dropout_rate, input_size):
    model = Sequential()
    model.add(Input(shape=input_size))
    model.add(Conv1D(32, 1, activation='relu', padding='same'))
    model.add(Conv1D(64, 1, activation='relu', padding='same'))
    model.add(MaxPooling1D(1))
    model.add(GRU(64))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    
    return model

def create_multi_cnn(dropout_rate, short_input_size, 
                          mid_input_size, long_input_size):
    short = Input(shape=short_input_size)
    mid = Input(shape=mid_input_size)
    long = Input(shape=long_input_size)
    
    x = Conv1D(32, 2, activation='relu', padding='same')(short)
    x = MaxPooling1D(2, padding='same')(x)
    x = Flatten()(x)
    x = Model(inputs=short, outputs=x)
    
    x2 = Conv1D(32, 2, activation='tanh', padding='same')(mid)
    x2 = MaxPooling1D(2, padding='same')(x2)
    x2 = Flatten()(x2)
    x2 = Model(inputs=mid, outputs=x2)

    x3 = Conv1D(32, 2, activation='tanh', padding='same')(long)
    x3 = MaxPooling1D(2, padding='same')(x3)
    x3 = Flatten()(x3)
    x3 = Model(inputs=long, outputs=x3)
    
    y = concatenate([x.output,x2.output,x3.output])
    y = Dense(128)(y)
    y = Dense(2, activation='softmax')(y)
    model = Model(inputs=[x.input, x2.input, x3.input], outputs=y)
    
    return model

def create_multi_cnn_lstm(dropout_rate, short_input_size, 
                          mid_input_size, long_input_size, concat):
    short = Input(shape=short_input_size)
    mid = Input(shape=mid_input_size)
    long = Input(shape=long_input_size)
    
    x = Conv1D(32, 2, activation='relu', padding='same')(short)
    x = MaxPooling1D(2, padding='same')(x)
    x = Flatten()(x)
    x = Model(inputs=short, outputs=x)
    
    x2 = Conv1D(32, 2, activation='relu', padding='same')(mid)
    x2 = MaxPooling1D(2, padding='same')(x2)
    x2 = Flatten()(x2)
    x2 = Model(inputs=mid, outputs=x2)

    x3 = Conv1D(32, 2, activation='relu', padding='same')(long)
    x3 = MaxPooling1D(2, padding='same')(x3)
    x3 = Flatten()(x3)
    x3 = Model(inputs=long, outputs=x3)
    
    y = concatenate([x.output,x2.output,x3.output])
    y = tf.reshape(y, (-1, concat, 1))
    y = LSTM(64, return_sequences=True)(y)
    y = LSTM(128)(y)
    y = Dense(128, activation='relu')(y)
    y = Dense(64, activation='relu')(y)
    y = Dense(2, activation='softmax')(y)
    model = Model(inputs=[x.input, x2.input, x3.input], outputs=y)
    
    return model

def create_multi_cnn_gru(dropout_rate, short_input_size, 
                          mid_input_size, long_input_size, concat):
    short = Input(shape=short_input_size)
    mid = Input(shape=mid_input_size)
    long = Input(shape=long_input_size)
    
    x = Conv1D(32, 2, activation='relu', padding='same')(short)
    x = MaxPooling1D(2, padding='same')(x)
    x = Flatten()(x)
    x = Model(inputs=short, outputs=x)
    
    x2 = Conv1D(32, 2, activation='relu', padding='same')(mid)
    x2 = MaxPooling1D(2, padding='same')(x2)
    x2 = Flatten()(x2)
    x2 = Model(inputs=mid, outputs=x2)

    x3 = Conv1D(32, 2, activation='relu', padding='same')(long)
    x3 = MaxPooling1D(2, padding='same')(x3)
    x3 = Flatten()(x3)
    x3 = Model(inputs=long, outputs=x3)
    
    y = concatenate([x.output,x2.output,x3.output])
    y = tf.reshape(y, (-1, concat, 1))
    y = GRU(64, return_sequences=True)(y)
    y = GRU(128)(y)
    y = Dense(128, activation='relu')(y)
    y = Dense(64, activation='relu')(y)
    y = Dense(2, activation='softmax')(y)
    model = Model(inputs=[x.input, x2.input, x3.input], outputs=y)
    
    return model

def create_model(model_n, dropout_rate, multi_input=False, x_train=None, short_x_train = None, mid_x_train = None, long_x_train = None, concat = None):
    if not multi_input:
        input_size = (x_train.shape[1], x_train.shape[2])
    else:
        short_input_size = (short_x_train.shape[1], short_x_train.shape[2])
        mid_input_size = (mid_x_train.shape[1], mid_x_train.shape[2])
        long_input_size = (long_x_train.shape[1], long_x_train.shape[2])
    
    if model_n == 'dnn':
        model = create_dnn(dropout_rate, input_size)
    elif model_n == 'cnn':
        model = create_cnn(dropout_rate, input_size)
    elif model_n == 'rnn':
        model = create_rnn(dropout_rate, input_size)
    elif model_n == 'lstm':
        model = create_lstm(dropout_rate, input_size)
    elif model_n == 'gru':
        model = create_gru(dropout_rate, input_size)
    elif model_n == 'cnn-rnn':
        model = create_cnn_rnn(dropout_rate, input_size)
    elif model_n == 'cnn-lstm':
        model = create_cnn_lstm(dropout_rate, input_size)
    elif model_n == 'cnn-gru':
        model = create_cnn_gru(dropout_rate, input_size)
    elif model_n == 'multi-cnn':
        model = create_multi_cnn(dropout_rate, short_input_size,
                                     mid_input_size, long_input_size)
    elif model_n == 'multi-cnn-lstm':
        model = create_multi_cnn_lstm(dropout_rate, short_input_size,
                                     mid_input_size, long_input_size, concat)
    elif model_n == 'multi-cnn-gru':
        model = create_multi_cnn_gru(dropout_rate, short_input_size,
                                     mid_input_size, long_input_size, concat)
    else:
        print('No Model')
        return None
    
    model.compile(optimizer='adam',
                 loss='categorical_crossentropy',
                 metrics=['acc'])
    
    return model